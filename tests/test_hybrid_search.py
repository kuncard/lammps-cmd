"""Test RRF fusion + GraphBooster (both modes)."""
import pytest
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent


# ── RRF fusion (tested via HybridRetriever or inline logic) ──

def _rrf_fuse(bm25_results, vec_results, rrf_k=60):
    """Inline RRF for unit testing — mirrors HybridRetriever.search logic."""
    rrf = {}
    bm25_map, vec_map = {}, {}
    id_to_chunk = {}

    for rank, r in enumerate(bm25_results):
        rrf[r["id"]] = rrf.get(r["id"], 0) + 1.0 / (rrf_k + rank + 1)
        bm25_map[r["id"]] = rank + 1
        id_to_chunk[r["id"]] = r

    for rank, r in enumerate(vec_results):
        rrf[r["id"]] = rrf.get(r["id"], 0) + 1.0 / (rrf_k + rank + 1)
        vec_map[r["id"]] = rank + 1
        if r["id"] not in id_to_chunk:
            id_to_chunk[r["id"]] = r

    sorted_items = sorted(rrf.items(), key=lambda x: x[1], reverse=True)
    results, seen = [], set()
    for cid, _ in sorted_items:
        chunk = id_to_chunk.get(cid)
        if not chunk:
            continue
        cmd = chunk.get("cmd_id", cid)
        if cmd in seen:
            continue
        seen.add(cmd)
        results.append({
            **chunk,
            "rrf_score": round(rrf[cid], 4),
            "bm25_rank": bm25_map.get(cid),
            "vec_rank": vec_map.get(cid),
        })
    return results


def test_rrf_empty_inputs():
    assert _rrf_fuse([], []) == []


def test_rrf_bm25_only():
    bm25 = [
        {"id": "a__1", "cmd_id": "fix_nh", "text": "nvt thermostat", "score": 10.0},
        {"id": "b__1", "cmd_id": "velocity", "text": "velocity create", "score": 5.0},
    ]
    results = _rrf_fuse(bm25, [])
    assert len(results) == 2
    assert results[0]["cmd_id"] == "fix_nh"


def test_rrf_dedups_by_cmd_id():
    """Two chunks with same cmd_id → only one survives."""
    bm25 = [
        {"id": "a__full", "cmd_id": "fix_nh", "text": "full doc", "score": 10.0},
        {"id": "a__syntax", "cmd_id": "fix_nh", "text": "syntax", "score": 5.0},
    ]
    results = _rrf_fuse(bm25, [])
    assert len(results) == 1
    assert results[0]["id"] == "a__full"  # first seen wins


def test_rrf_merges_both_sources():
    """RRF should interleave BM25 + vector results."""
    bm25 = [
        {"id": "a__1", "cmd_id": "fix_nh", "text": "nvt", "score": 10.0},
        {"id": "c__1", "cmd_id": "compute_temp", "text": "temp", "score": 5.0},
    ]
    vec = [
        {"id": "b__1", "cmd_id": "fix_langevin", "text": "langevin", "score": 0.9},
    ]
    results = _rrf_fuse(bm25, vec)
    cmd_ids = {r["cmd_id"] for r in results}
    assert "fix_nh" in cmd_ids
    assert "fix_langevin" in cmd_ids
    assert "compute_temp" in cmd_ids


# ── GraphBooster ──

from hybrid_search import GraphBooster


class TestGraphBoosterRerank:
    """Conservative mode: re-rank existing results only, no new nodes."""

    def test_empty_results(self):
        gb = GraphBooster(mode="rerank")
        assert gb.boost([]) == []

    def test_no_new_nodes(self):
        gb = GraphBooster(mode="rerank")
        results = [
            {"cmd_id": "fix_nh", "title": "fix nvt", "score": 10.0},
            {"cmd_id": "velocity", "title": "velocity", "score": 8.0},
        ]
        boosted = gb.boost(results)
        cmd_ids = {r["cmd_id"] for r in boosted}
        assert cmd_ids == {"fix_nh", "velocity"}  # no new nodes

    def test_boost_preserves_order(self):
        gb = GraphBooster(mode="rerank")
        results = [
            {"cmd_id": "fix_nh", "title": "fix nvt", "score": 10.0},
            {"cmd_id": "velocity", "title": "velocity", "score": 8.0},
        ]
        boosted = gb.boost(results, top_k=5)
        assert len(boosted) <= 5
        # fix_nh should still be first (it has the highest score)
        assert boosted[0]["cmd_id"] == "fix_nh"


class TestGraphBoosterExpand:
    """Aggressive mode: can introduce neighbor nodes."""

    def test_empty_results(self):
        gb = GraphBooster(mode="expand")
        assert gb.boost([]) == []

    def test_top_k_truncation(self):
        gb = GraphBooster(mode="expand")
        results = [
            {"cmd_id": "fix_nh", "title": "fix nvt", "score": 10.0},
        ]
        boosted = gb.boost(results, top_k=2)
        assert len(boosted) <= 2


def test_graph_booster_lazy_loads_graph():
    """Calling boost() triggers graph load automatically."""
    gb = GraphBooster(mode="rerank")
    assert gb._adj is None
    gb.boost([])  # triggers _ensure_loaded
    # _ensure_loaded sets _adj to {} if file missing, or populated dict
    assert gb._adj is not None
