"""
Hybrid retrieval: BM25 + vector search with RRF (Reciprocal Rank Fusion) + graph boost.

Usage:
  python hybrid_search.py "how to set up NPT with anisotropic pressure"
"""
import argparse, json
from pathlib import Path
from collections import defaultdict
from bm25_index import BM25Index
from vector_index import VectorIndex

ROOT = Path(__file__).parent


# ═══════════════════════════════════════════════════════════════════════
#  Unified GraphBooster — shared by Flask (hybrid_search) and CLI (search_lammps)
# ═══════════════════════════════════════════════════════════════════════

class GraphBooster:
    """Applies knowledge-graph edge information to re-rank or expand search results.

    Two modes:
      - 'rerank' (default): boost existing results only. Safer for UI — no
        new nodes introduced, just reorder what text search already found.
      - 'expand': allow neighbor nodes NOT in original results to appear.
        Useful for CLI where completeness matters and false positives are
        filtered downstream.

    Both modes share the same adjacency data from graph_data_full.json.
    """

    def __init__(self, graph_path=None, mode="rerank"):
        self._graph_path = Path(graph_path or ROOT / "graph_data_full.json")
        self._mode = mode
        self._adj = None          # cmd_id → [(neighbor_cmd_id, edge_type, weight), ...]
        self._node_info = {}      # cmd_id → {title, url}

    # ── lazy load ──
    def _ensure_loaded(self):
        if self._adj is not None:
            return
        if not self._graph_path.exists():
            self._adj = {}
            return
        with open(self._graph_path, encoding="utf-8") as f:
            g = json.load(f)
        self._adj = defaultdict(list)
        for n in g["nodes"]:
            self._node_info[n["id"]] = {
                "title": n.get("title", n["id"]),
                "url": n.get("url", ""),
            }
        for e in g["edges"]:
            w = e.get("weight", 3)
            etype = e.get("type", "related")
            self._adj[e["from"]].append((e["to"], etype, w))
            self._adj[e["to"]].append((e["from"], etype, w))

    # ── boost ──
    def boost(self, results, top_k=None):
        """Apply graph boost. Returns reordered results (and possibly new nodes in expand mode)."""
        self._ensure_loaded()
        if not self._adj or not results:
            return results[:top_k] if top_k else list(results)

        if self._mode == "rerank":
            return self._boost_rerank(results, top_k)
        else:
            return self._boost_expand(results, top_k)

    def _boost_rerank(self, results, top_k):
        """Conservative: re-rank existing results by graph connectivity.

        Each result 'votes' for its graph neighbors. Higher-ranked results
        contribute more (rank decay), and higher-weight edges contribute more.
        The boost is multiplicative so it can't push a weak match past a strong one.
        """
        boosts = defaultdict(float)
        max_score = max((r.get("score", 0) for r in results), default=1)

        for rank, r in enumerate(results):
            nid = r.get("cmd_id", "")
            decay = 1.0 / (1.0 + rank * 0.5)          # rank0=1.0, rank1=0.67, …
            base = r.get("score", 0) / max(max_score, 1) * 3 * decay
            for nb, _etype, weight in self._adj.get(nid, []):
                boost = base * weight / 30.0
                boosts[nb] = max(boosts[nb], boost)    # keep strongest signal

        for r in results:
            nid = r.get("cmd_id", "")
            if nid in boosts and boosts[nid] > 0:
                r["graph_boost"] = round(boosts[nid], 4)
                r["score"] = r.get("score", 0) * (1.0 + boosts[nid])

        results.sort(key=lambda r: r.get("score", 0), reverse=True)
        return results[:top_k] if top_k else results

    def _boost_expand(self, results, top_k):
        """Aggressive: allow neighbor nodes to enter the result set.

        Each result's score propagates along graph edges. Nodes that were
        missed by text search but are strongly connected to top results
        get assigned a synthetic score.
        """
        boosts = defaultdict(float)
        rtypes = defaultdict(set)

        for r in results:
            nid = r.get("cmd_id", r.get("id", ""))
            bs = r.get("score", 0)
            for nb, etype, weight in self._adj.get(nid, []):
                boosts[nb] += bs * (weight / 100.0)
                rtypes[nb].add(etype)

        # Start with existing results (deduped)
        scored, seen = [], set()
        for r in results:
            nid = r.get("cmd_id", r.get("id", ""))
            if nid in seen:
                continue
            seen.add(nid)
            r2 = dict(r)
            r2["graph_boost"] = 0
            r2["_neighbor_of"] = ""
            scored.append(r2)

        # Inject neighbor nodes surfaced by graph
        for nid, b in boosts.items():
            if nid in seen:
                continue
            seen.add(nid)
            info = self._node_info.get(nid, {})
            scored.append({
                "cmd_id": nid,
                "title": info.get("title", nid),
                "section": "neighbor",
                "score": round(b, 4),
                "graph_boost": round(b, 4),
                "text": "",
                "url": info.get("url", f"https://docs.lammps.org/{nid}.html"),
                "_neighbor_of": ", ".join(sorted(rtypes.get(nid, set()))),
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k] if top_k else scored


# ── Legacy module-level wrapper (kept for backwards compat) ──

def _graph_boost(results, top_k):
    """Thin wrapper → GraphBooster(mode='rerank').boost()."""
    booster = GraphBooster(mode="rerank")
    return booster.boost(results, top_k)


# ═══════════════════════════════════════════════════════════════════════
#  Shared RRF Fusion
# ═══════════════════════════════════════════════════════════════════════

def rrf_fuse(ranked_lists, rrf_k=60, key_fn=None, dedup_key_fn=None,
             top_k=None, annotate=True):
    """Fuse multiple ranked result lists via Reciprocal Rank Fusion.

    Args:
        ranked_lists: list of [(list_of_dicts, source_name), ...]
                      Each inner list is independently ranked (best first).
        rrf_k: RRF constant (60 = standard, >60 = less weight to rank).
        key_fn: callable(r) → RRF merge key (e.g. chunk id or cmd_id).
                Default: r.get("cmd_id", r.get("id", "")).
        dedup_key_fn: callable(r) → dedup key, or None to use same as key_fn.
                      (e.g. cmd_id when RRFing by chunk-id).
        top_k: return at most this many results (None = all).
        annotate: if True, add bm25_rank/bm25_score/vec_rank/vec_score fields
                  (Flask-style). If False, minimal output (CLI-style).

    Returns:
        List of merged dicts with 'rrf_score', sorted by RRF score desc.
    """
    if key_fn is None:
        key_fn = lambda r: r.get("cmd_id", r.get("id", ""))

    rrf_scores = {}
    key_to_result = {}
    source_ranks = {}  # key → [(source_idx, rank, score), ...]

    for src_idx, (src_results, _src_name) in enumerate(ranked_lists):
        for rank, r in enumerate(src_results):
            key = key_fn(r)
            rrf_scores[key] = rrf_scores.get(key, 0) + 1.0 / (rrf_k + rank + 1)
            if key not in key_to_result:
                key_to_result[key] = r
            source_ranks.setdefault(key, []).append((src_idx, rank + 1, r.get("score", 0)))

    if not rrf_scores:
        return []

    sorted_keys = sorted(rrf_scores, key=lambda k: rrf_scores[k], reverse=True)

    merged = []
    dedup_seen = set()
    for key in sorted_keys:
        chunk = key_to_result.get(key)
        if not chunk:
            continue

        dk = dedup_key_fn(chunk) if dedup_key_fn else key
        if dk in dedup_seen:
            continue
        dedup_seen.add(dk)

        result = dict(chunk)
        result["rrf_score"] = round(rrf_scores[key], 4)

        if annotate:
            sr = source_ranks.get(key, [])
            # Map source_idx → field name for backward compat
            for si, rank, score in sr:
                if si == 0:
                    result["bm25_rank"] = rank
                    result["bm25_score"] = score
                elif si == 1:
                    result["vec_rank"] = rank
                    result["vec_score"] = score

        merged.append(result)

        if top_k and len(merged) >= top_k:
            break

    return merged


# ═══════════════════════════════════════════════════════════════════════
#  HybridRetriever
# ═══════════════════════════════════════════════════════════════════════

class HybridRetriever:
    """Combines BM25 and vector search via RRF + graph boost."""

    def __init__(self, bm25=None, vector=None, expander=None):
        self.bm25 = bm25
        self.vector = vector
        self.expander = expander  # optional QueryExpander for Flask path

    def search(self, query, top_k=5, per_index=20, rrf_k=None, query_type="command"):
        """RRF hybrid search with graph boost. Returns top_k chunks, deduped by cmd_id.

        rrf_k is auto-tuned by query_type if not explicitly set:
          command → 80 (BM25 leads), natural → 20 (vector leads), param → 60
        """
        # Apply graph-based query expansion if available
        if self.expander:
            query = self.expander.expand(query)

        # Auto-tune RRF k by query type (only when not explicitly set)
        if rrf_k is None:
            rrf_k = {"command": 80, "natural": 20, "param": 60}.get(query_type, 60)

        # Get results from both indexes
        bm25_results = self.bm25.search(query, limit=per_index, query_type=query_type) if self.bm25 else []
        vec_results = self.vector.search(query, top_k=per_index) if self.vector else []

        # RRF fusion: key by chunk-id, dedup by cmd_id
        results = rrf_fuse(
            [(bm25_results, "bm25"), (vec_results, "vector")],
            rrf_k=rrf_k,
            key_fn=lambda r: r.get("id", ""),
            dedup_key_fn=lambda r: r.get("cmd_id", ""),
            top_k=top_k,
            annotate=True,
        )

        # Graph boost: surface related commands
        results = _graph_boost(results, top_k)

        return results


def load_retriever():
    """Load BM25 and vector indexes, return HybridRetriever."""
    bm25 = BM25Index()
    bm25.load()
    vec = VectorIndex()
    vec.load()
    return HybridRetriever(bm25, vec)


# ── CLI ──
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("query", type=str)
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()

    retriever = load_retriever()
    results = retriever.search(args.query, top_k=args.limit)

    print(f"\nQuery: {args.query}\n")
    for i, r in enumerate(results):
        print(f"[{i+1}] {r['title']} / {r['section']}")
        print(f"    RRF={r['rrf_score']:.4f}  BM25=#{r['bm25_rank']}  Vec=#{r['vec_rank']}")
        print(f"    {r['text'][:150]}...")
        print(f"    {r['url']}")
        print()
