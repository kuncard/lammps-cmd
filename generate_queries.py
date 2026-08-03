"""
Auto-generate evaluation queries from graph_data_full.json edges.

Usage:
  python generate_queries.py              # generate queries
  python generate_queries.py --llm        # also generate LLM natural queries (needs API key)
"""
import json, random, os
from pathlib import Path
from collections import defaultdict

from logging_setup import setup_logging
log = setup_logging(__name__)

ROOT = Path(__file__).parent
GRAPH = ROOT / "graph_data_full.json"
OUTPUT = ROOT / "golden_queries_auto.json"  # auto-generated only — never mix with hand-crafted
random.seed(42)


def load_graph():
    with open(GRAPH, encoding="utf-8") as f:
        g = json.load(f)
    nodes = {n["id"]: n for n in g["nodes"]}
    edges = g["edges"]
    # Group edges by type
    by_type = defaultdict(list)
    for e in edges:
        by_type[e["type"]].append(e)
    return nodes, by_type


def pick_popular(nodes, edges_by_type, n=30):
    """Pick the most-connected nodes as query subjects."""
    degree = defaultdict(int)
    for etype_edges in edges_by_type.values():
        for e in etype_edges:
            degree[e["from"]] += 1
            degree[e["to"]] += 1
    popular = sorted(degree.items(), key=lambda x: x[1], reverse=True)
    # Prefer fix/compute/pair category nodes
    popular_cmds = [(nid, d) for nid, d in popular
                    if any(nid.startswith(p) for p in ("fix_", "compute_", "pair_", "kspace_", "dump_"))]
    return popular_cmds[:n]


def generate_queries(nodes, edges_by_type, n_per_type=30):
    """Generate evaluation queries from graph edges."""
    queries = []
    popular = pick_popular(nodes, edges_by_type, n=50)
    popular_ids = {p[0] for p in popular}

    # 1. "requires" queries: X needs Y
    requires = edges_by_type.get("requires", [])
    sampled = [e for e in requires if e["from"] in popular_ids][:n_per_type]
    for e in sampled:
        src_title = nodes[e["from"]]["title"]
        tgt_title = nodes[e["to"]]["title"]
        queries.append({
            "category": "graph_requires",
            "query": f"what does {src_title} require",
            "expected_ids": [e["to"]],
        })
        queries.append({
            "category": "graph_requires",
            "query": f"prerequisites for {src_title}",
            "expected_ids": [e["to"]],
        })

    # 2. "alternative" queries: X vs Y
    alternatives = edges_by_type.get("alternative", [])
    sampled = [e for e in alternatives if e["from"] in popular_ids][:n_per_type]
    for e in sampled:
        src_title = nodes[e["from"]]["title"]
        tgt_title = nodes[e["to"]]["title"]
        queries.append({
            "category": "graph_alternative",
            "query": f"{src_title} vs {tgt_title}",
            "expected_ids": [e["from"], e["to"]],
        })
        queries.append({
            "category": "graph_alternative",
            "query": f"difference between {src_title} and {tgt_title}",
            "expected_ids": [e["from"], e["to"]],
        })

    # 3. "related" queries: X and Y together
    related = edges_by_type.get("related", [])
    sampled = [e for e in related if e["from"] in popular_ids and e["to"] in popular_ids][:n_per_type]
    for e in sampled:
        src_title = nodes[e["from"]]["title"]
        tgt_title = nodes[e["to"]]["title"]
        queries.append({
            "category": "graph_related",
            "query": f"{src_title} and {tgt_title}",
            "expected_ids": [e["from"], e["to"]],
        })

    # 4. "creates" queries: what does X create/output
    creates = edges_by_type.get("creates", [])
    sampled = [e for e in creates if e["from"] in popular_ids][:n_per_type]
    for e in sampled:
        src_title = nodes[e["from"]]["title"]
        queries.append({
            "category": "graph_creates",
            "query": f"what does {src_title} output",
            "expected_ids": [e["to"]],
        })

    # 5. Command lookup by category
    by_category = defaultdict(list)
    for n in nodes.values():
        cat = n.get("category", "other")
        by_category[cat].append(n)

    for cat, cat_nodes in by_category.items():
        if len(cat_nodes) < 3:
            continue
        sample = random.sample(cat_nodes, min(5, len(cat_nodes)))
        for n in sample:
            queries.append({
                "category": "command_lookup",
                "query": f"how to use {n['title']}",
                "expected_ids": [n["id"]],
            })

    return queries


def merge_with_existing(new_queries, existing_path):
    """Merge new queries with existing ones, avoid duplicates by query text."""
    if existing_path.exists():
        with open(existing_path, encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing_texts = {q["query"] for q in existing}
    added = 0
    for q in new_queries:
        if q["query"] not in existing_texts:
            existing.append(q)
            existing_texts.add(q["query"])
            added += 1

    return existing, added


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", action="store_true", help="Also generate LLM natural queries")
    ap.add_argument("--llm-limit", type=int, default=30)
    args = ap.parse_args()

    nodes, edges_by_type = load_graph()

    # Generate template queries from graph edges
    new_queries = generate_queries(nodes, edges_by_type, n_per_type=25)
    log.info("Generated %s graph-template queries", len(new_queries))

    # Optionally generate LLM queries
    if args.llm:
        api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        if api_key:
            log.info("Generating LLM natural-language queries...")
            llm_queries = generate_llm_queries(nodes, api_key, limit=args.llm_limit)
            new_queries.extend(llm_queries)
            log.info("  +%s LLM queries", len(llm_queries))
        else:
            log.warning("Set DEEPSEEK_API_KEY for LLM query generation")

    # Merge with existing
    merged, added = merge_with_existing(new_queries, OUTPUT)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    log.info("Merged: %s total (%s new)", len(merged), added)
