#!/usr/bin/env python
"""
LAMMPS Knowledge Graph Search — 5-layer pipeline.
Reads graph_data_full.json + lammps_kb/*.md. Imports BM25 + spell from root.

Pipeline: abbreviation → graph query expansion → spell correction → stemming → BM25 → graph boost

Usage:
  python search_lammps.py search "nvt thermostat" --limit 5
  python search_lammps.py suggest "ther"
  python search_lammps.py health
  python search_lammps.py detail fix_nh
  python search_lammps.py neighbors fix_nh

All commands print JSON to stdout.
"""
import json, re, argparse, sys
from pathlib import Path
from collections import defaultdict

# ── Paths ──
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent.parent.parent  # skills/lammps-kg/scripts/ → root

# Import shared utilities from root bm25_index (avoids duplication)
sys.path.insert(0, str(ROOT))
from bm25_index import (
    BM25Index, tokenize, STOP_WORDS as STOPS,
    classify_query as _classify_query,
)
GRAPH_FILE = ROOT / "graph_data_full.json"
KB_DIR = ROOT / "lammps_kb"
KB_SUBDIRS = [KB_DIR / d for d in ["fix","compute","pair","bond","angle","dihedral","improper","dump","kspace","howto","general"] if (KB_DIR / d).exists()]

# ── Utils ──
def clean_text(s):
    """Strip non-ASCII and control chars that break JSON encoding."""
    return s.encode("ascii", errors="replace").decode("ascii").replace("?", " ")

# ── 1. Abbreviation Expansion (shared single source of truth) ──
from abbrev import ABBREV, PHRASE_MAP
# Sort by length descending: lj/cut must match before lj
ABBREV_KEYS = sorted(ABBREV, key=len, reverse=True)
ABBREV_RE = re.compile(r'\b(' + '|'.join(re.escape(k) for k in ABBREV_KEYS) + r')\b', re.IGNORECASE)

def expand_abbreviations(query):
    """Expand abbreviations + multi-word phrases in query text."""
    # 1. Phrase-level expansion (shared PHRASE_MAP from abbrev.py)
    ql = query.lower()
    for phrase, expansion in PHRASE_MAP:
        if phrase in ql:
            query = query + " " + expansion
    # 2. Single-word abbreviation expansion
    def _replace(m):
        w = m.group(0).lower()
        return ABBREV.get(w, m.group(0))
    return ABBREV_RE.sub(_replace, query)


# ── 1.5. Graph-based Query Expansion (extracted to query_expander.py) ──
from query_expander import QueryExpander


# ── 2. Stemming ──
def stem(word):
    if len(word) <= 4: return word
    for pat, rep in [
        (r"(ational|tional|al|tion|sion|ment|ness|ship|hood)$", ""),
        (r"(able|ible|ful|less|ous|ive|ish|ant|ent|ism|ist)$", ""),
        (r"(ity|ty|ence|ance|ure|ery|ory|ary|ate|ize|ify)$", ""),
        (r"(?<=\w)(isation|ization|iser|izer|ability)$", ""),
        (r"(?<=\w)(s|es|ed|er|est|ly|ing)$", ""),
    ]:
        w2 = re.sub(pat, rep, word)
        if w2 != word and len(w2) >= 4:
            return w2
    return word


# ── 4. Graph Booster (unified implementation in hybrid_search.py) ──
from hybrid_search import GraphBooster, rrf_fuse


# ── 6. Data loading ──
def load_data():
    with open(GRAPH_FILE, encoding="utf-8") as f:
        g = json.load(f)
    nodes, edges = g["nodes"], g["edges"]
    kb = {}
    if KB_DIR.exists():
        for mp in sorted(list(KB_DIR.glob("*.md")) + list(KB_DIR.rglob("*/*.md"))):
            with open(mp, encoding="utf-8") as f:
                md = f.read()
            fid = mp.stem
            m = re.match(r"^---\n.*?\nid:\s*(\S+).*?\n---", md, re.DOTALL)
            if m: fid = m.group(1)
            body = re.sub(r"^---[\s\S]*?---\n*","",md)
            body = re.sub(r"```[\s\S]*?```","",body)
            body = re.sub(r"\*\*(.+?)\*\*",r"\1",body)
            body = re.sub(r"\[(.+?)\]\(.*?\)",r"\1",body)
            body = re.sub(r"[#*>\-|`]"," ",body)
            kb[fid] = clean_text(body)
    return nodes, edges, kb

def build_index(nodes, edges, kb):
    docs = []
    for n in nodes:
        st = f"{n.get('title','')} {n.get('synopsis','')} {n.get('syntax','')} {n.get('description','')} "
        st += " ".join(n.get("examples",[])) + " "
        kw = n.get("keywords",{})
        if isinstance(kw,dict):
            st += " ".join(kw.keys())+" "
            for v in kw.values():
                if isinstance(v,dict): st += v.get("desc","")+" "+v.get("options","")+" "
                elif isinstance(v,str): st += v+" "
        st += n.get("restrictions","")
        st = clean_text(st)
        docs.append({"id":f"{n['id']}__struct","cmd_id":n["id"],"title":n.get("title",n["id"]),
            "section":"structured","url":n.get("url",f"https://docs.lammps.org/{n['id']}.html"),
            "phase":n.get("phase",""),"text":st})
        mt = kb.get(n["id"],"")
        if len(mt)>50:
            docs.append({"id":f"{n['id']}__manual","cmd_id":n["id"],"title":n.get("title",n["id"]),
                "section":"manual","url":n.get("url",f"https://docs.lammps.org/{n['id']}.html"),
                "phase":n.get("phase",""),"text":mt})
    bm25 = BM25Index(); bm25.build(docs)
    expander = QueryExpander(nodes, edges)
    return bm25, GraphBooster(mode="expand"), expander

_BM25 = _GRAPH = _EXPANDER = _NODES = _EDGES = _KB = None
def _init():
    global _BM25,_GRAPH,_EXPANDER,_NODES,_EDGES,_KB
    if _BM25 is not None: return
    _NODES,_EDGES,_KB = load_data()
    _BM25,_GRAPH,_EXPANDER = build_index(_NODES,_EDGES,_KB)


# ── 7. Query Type Classification (thin wrapper around shared classifier) ──
_CMDSET = None  # lazily built set of known command words from graph


def _get_cmdset():
    """Build a set of known command IDs / tokens from graph nodes.

    Feeds into shared classify_query() for precise command-name detection.
    """
    global _CMDSET
    if _CMDSET is not None:
        return _CMDSET
    _CMDSET = set()
    _init()
    for n in _NODES:
        _CMDSET.add(n["id"])
        # Also add individual words from IDs: fix_nh → {"fix_nh","fix","nh"}
        parts = n["id"].split("_")
        for p in parts:
            if len(p) >= 2:
                _CMDSET.add(p)
        # Add title words
        title_words = n.get("title", "").lower().split()
        for w in title_words:
            w = w.strip()
            if len(w) >= 2 and w not in ("command", "style"):
                _CMDSET.add(w)
    return _CMDSET


def classify_query(query):
    """Classify a query using the shared classifier with graph-awareness."""
    return _classify_query(query, known_commands=_get_cmdset())


# ── 8. Vector Search (delegates to shared VectorIndex) ──
_VEC_INDEX = None  # lazily loaded VectorIndex instance


def _init_vector():
    """Load pre-built vector index (reuses vector_index.VectorIndex)."""
    global _VEC_INDEX
    if _VEC_INDEX is not None:
        return True
    from vector_index import VectorIndex
    vi = VectorIndex()
    if not vi.load():
        return False
    _VEC_INDEX = vi
    return True


def _vector_search(query, top_k=20):
    """Cosine similarity search via shared VectorIndex."""
    if _VEC_INDEX is None:
        return []
    return _VEC_INDEX.search(query, top_k=top_k)


# ── 9. Pipeline ──
def search(query, limit=10, phase=None, verbose=False, use_vector=False):
    _init()
    original_query = query  # keep for vector search (unpolluted by expansions)
    query = expand_abbreviations(query)
    query = _EXPANDER.expand(query)

    # Classify query type → adjust retrieval strategy
    qtype, qparams = classify_query(query)
    search_limit = max(qparams.get("bm25_limit", 10), limit * 2)

    qt = tokenize(query)
    corr = []
    for t in qt:
        c, sc = _BM25.spell.correct(t)
        corr.append(c if sc > 0.5 else t)
    cq = " ".join(corr)
    sq = " ".join(stem(t) for t in corr)

    # For natural language queries, use corrected+stemmed query together
    # For command queries, use original (abbrev-expanded) query primarily
    if qtype == "natural":
        aq = f"{cq} {sq} {query}"
    else:
        aq = f"{query} {cq} {sq}"

    results = _BM25.search(aq, limit=search_limit, query_type=qtype, expand=False)

    # Section boost for parameter queries (structured docs have syntax info)
    if qparams.get("section_boost") == "structured":
        for r in results:
            if r.get("section") == "structured":
                r["score"] = r.get("score", 0) * 1.15

    # Vector search → RRF merge with BM25 (use original query, not expanded)
    if use_vector and _init_vector():
        vec_results = _vector_search(original_query, top_k=search_limit)
        if vec_results:
            # RRF: use cmd_id as key (BM25 docs and vector chunks share cmd_id)
            cli_rrf_k = 20 if qtype == "natural" else 60
            merged = rrf_fuse(
                [(results, "bm25"), (vec_results, "vector")],
                rrf_k=cli_rrf_k,
                key_fn=lambda r: r.get("cmd_id", r.get("id", "")),
                top_k=search_limit,
                annotate=False,
            )
            # Scale RRF score up for downstream graph boost
            for r in merged:
                r["score"] = round(r["rrf_score"] * 100, 4)
            results = merged

    if phase and phase != "all":
        results = [r for r in results if r.get("phase") == phase]

    boosted = _GRAPH.boost(results)[:limit]
    out = {"query": query, "corrected": cq if cq != query else None,
           "expanded": bool(ABBREV_RE.search(query)),
           "query_type": qtype,
           "vector_enabled": bool(use_vector and _VEC_INDEX is not None),
           "total": len(boosted), "results": []}
    for i, r in enumerate(boosted):
        it = {"rank": i + 1, "cmd_id": r.get("cmd_id", ""), "title": r.get("title", ""),
              "section": r.get("section", ""), "score": r.get("score", 0),
              "url": r.get("url", ""),
              "text_preview": (r.get("text", "") or "")[:400]}
        if r.get("graph_boost", 0) > 0:
            it["graph_boost"] = r["graph_boost"]
            it["neighbor_of"] = r.get("_neighbor_of", "")
        if verbose:
            it["text"] = r.get("text", "")
            it["phase"] = r.get("phase", "")
        out["results"].append(it)
    return out

def suggest(prefix, limit=8):
    _init()
    prefix = prefix.lower().strip()
    if len(prefix)<2: return {"suggestions":[]}
    cand = set()
    for n in _NODES:
        if prefix in n.get("title","").lower(): cand.add(n["title"])
        if prefix in n["id"].lower(): cand.add(n["id"])
        kw = n.get("keywords",{})
        if isinstance(kw,dict):
            for k in kw:
                if prefix in k.lower(): cand.add(k)
    for a,e in ABBREV.items():
        if prefix in a: cand.add(f"{a} -> {e[:50]}")
    return {"suggestions": sorted(cand, key=lambda s:(len(s),s.lower()))[:limit]}

def health():
    _init()
    expander_terms = len(_EXPANDER.word_to_ids)
    return {"status":"ok","nodes":len(_NODES),"edges":len(_EDGES),
        "indexed_docs":_BM25.N,"vocab_size":len(_BM25.df),
        "avg_doc_len":round(_BM25.avgdl,1),"kb_articles":len(_KB),
        "abbreviations":len(ABBREV),
        "graph_expansions": expander_terms}

def detail(cmd_id):
    _init()
    node = next((n for n in _NODES if n["id"]==cmd_id),None)
    mc = ""
    mp = KB_DIR/f"{cmd_id}.md"
    if mp.exists():
        with open(mp,encoding="utf-8") as f: raw = f.read()
        mc = re.sub(r"^---[\s\S]*?---\n*","",raw).strip()
    if not node and not mc: return {"error":f"not found: {cmd_id}"}
    r = {"cmd_id":cmd_id}
    if node:
        for k in ["title","phase","url","syntax","description","keywords","examples","restrictions"]:
            r[k] = node.get(k,"")
    if mc: r["manual_content"] = clean_text(mc[:3000])
    return r

def neighbors(cmd_id):
    _init()
    grp = defaultdict(list)
    for e in _EDGES:
        if e["from"]==cmd_id:
            o = next((n for n in _NODES if n["id"]==e["to"]),None)
            grp[e.get("type","related")].append({"dir":"->","cmd":e["to"],
                "title":o["title"] if o else e["to"],"weight":e.get("weight",0),
                "source":e.get("source","")})
        if e["to"]==cmd_id:
            o = next((n for n in _NODES if n["id"]==e["from"]),None)
            grp[e.get("type","related")].append({"dir":"<-","cmd":e["from"],
                "title":o["title"] if o else e["from"],"weight":e.get("weight",0),
                "source":e.get("source","")})
    return {"cmd_id":cmd_id,"relationships":{k:v for k,v in grp.items()}}


# ── CLI ──
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="LAMMPS KG Search v2")
    ap.add_argument("cmd", choices=["search","suggest","health","detail","neighbors"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--limit", type=int, default=5); ap.add_argument("--phase", default=None)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--vector", action="store_true", help="Enable vector semantic search (requires numpy)")
    args = ap.parse_args()
    try:
        if args.cmd=="search":
            print(json.dumps(search(args.arg, args.limit, args.phase, args.verbose, use_vector=args.vector), ensure_ascii=False, indent=2))
        elif args.cmd=="suggest": print(json.dumps(suggest(args.arg), ensure_ascii=False, indent=2))
        elif args.cmd=="health": print(json.dumps(health(), ensure_ascii=False, indent=2))
        elif args.cmd=="detail": print(json.dumps(detail(args.arg), ensure_ascii=False, indent=2))
        elif args.cmd=="neighbors": print(json.dumps(neighbors(args.arg), ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error":str(e)}, ensure_ascii=False)); sys.exit(1)
