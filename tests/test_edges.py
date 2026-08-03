"""Test graph edge integrity."""
import json
from pathlib import Path
from collections import Counter

GRAPH_FULL = Path(__file__).parent.parent / "graph_data_full.json"


def load_graph(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def test_no_self_loops():
    if not GRAPH_FULL.exists():
        return
    g = load_graph(GRAPH_FULL)
    for e in g["edges"]:
        assert e["from"] != e["to"], f"Self-loop: {e['from']}"


def test_edges_reference_valid_nodes():
    if not GRAPH_FULL.exists():
        return
    g = load_graph(GRAPH_FULL)
    node_ids = {n["id"] for n in g["nodes"]}
    for e in g["edges"]:
        assert e["from"] in node_ids, f"Bad from: {e['from']}"
        assert e["to"] in node_ids, f"Bad to: {e['to']}"


def test_edge_types_valid():
    if not GRAPH_FULL.exists():
        return
    valid = {"requires", "incompatible", "creates", "alternative", "related", "howto_ref", "refers_to"}
    g = load_graph(GRAPH_FULL)
    for e in g["edges"]:
        assert e["type"] in valid, f"Bad type: {e['type']}"


def test_full_graph_if_exists():
    if not GRAPH_FULL.exists():
        return
    g = load_graph(GRAPH_FULL)
    assert len(g["nodes"]) >= 900
    assert len(g["edges"]) >= 1900
    for n in g["nodes"]:
        assert "phase" in n or "category" in n, f"Node {n['id']} missing phase/category"


def test_no_duplicate_node_ids():
    if not GRAPH_FULL.exists():
        return
    g = load_graph(GRAPH_FULL)
    ids = [n["id"] for n in g["nodes"]]
    dupes = [i for i, c in Counter(ids).items() if c > 1]
    assert not dupes, f"Duplicate node ids: {dupes}"


def test_edge_confidence_field():
    if not GRAPH_FULL.exists():
        return
    g = load_graph(GRAPH_FULL)
    for e in g["edges"]:
        if "confidence" in e:
            assert e["confidence"] in {"high", "medium", "low"}
