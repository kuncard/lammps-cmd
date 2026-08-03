"""
Search quality evaluation — runs golden queries against search_lammps.py.

Two query sets:
  - golden_queries_hand.json : hand-crafted, authoritative (weighted in final score)
  - golden_queries_auto.json : auto-generated from graph edges (consistency check only)

Usage:
  python evaluate.py               # evaluate both sets
  python evaluate.py --hand-only   # hand-crafted only
  python evaluate.py --vector      # enable vector search
"""
import json, sys, argparse
from pathlib import Path

from logging_setup import setup_logging
log = setup_logging(__name__)

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "skills" / "lammps-kg" / "scripts"))
from search_lammps import search

HAND_FILE = ROOT / "golden_queries_hand.json"
AUTO_FILE = ROOT / "golden_queries_auto.json"


def _load_queries(golden_file):
    """Load query set from JSON. Returns [] on failure."""
    gf = Path(golden_file)
    if not gf.exists():
        return []
    with open(gf, encoding="utf-8") as f:
        return json.load(f)


def _eval_set(queries, label, use_vector):
    """Evaluate one query set. Returns (top1, top3, total, per_category_stats)."""
    top1_hits, top3_hits, total = 0, 0, 0
    categories = {}

    for q in queries:
        total += 1
        cat = q.get("category", "general")
        if cat not in categories:
            categories[cat] = {"total": 0, "top1": 0, "top3": 0, "failures": []}
        categories[cat]["total"] += 1

        results = search(q["query"], limit=5, use_vector=use_vector)
        hit_ids = {r["cmd_id"] for r in results["results"]}
        expected_id = q.get("expected_id", "")
        expected_ids = q.get("expected_ids", [expected_id] if expected_id else [])

        if any(eid in hit_ids for eid in expected_ids):
            categories[cat]["top3"] += 1
            top3_hits += 1

            if results["results"] and results["results"][0]["cmd_id"] in expected_ids:
                categories[cat]["top1"] += 1
                top1_hits += 1
        else:
            top_hit = results["results"][0]["cmd_id"] if results["results"] else "NONE"
            categories[cat]["failures"].append({
                "query": q["query"],
                "expected": expected_ids,
                "got": top_hit
            })

    return top1_hits, top3_hits, total, categories


def _print_set_report(label, top1, top3, total, categories, show_failures=True):
    """Print a formatted evaluation report for one query set."""
    if total == 0:
        print(f"\n  [{label}] (no queries)\n")
        return

    t1_pct = top1 / total * 100 if total else 0
    t3_pct = top3 / total * 100 if total else 0
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Total queries: {total}")
    print(f"  Top-1:  {top1}/{total} = {t1_pct:.0f}%")
    print(f"  Top-3:  {top3}/{total} = {t3_pct:.0f}%")

    print(f"\n  By Category:")
    for cat, stats in sorted(categories.items()):
        t1 = stats["top1"] / stats["total"] * 100 if stats["total"] else 0
        t3 = stats["top3"] / stats["total"] * 100 if stats["total"] else 0
        print(f"    {cat:22s}  Top-1: {stats['top1']:>2}/{stats['total']:<2} ({t1:3.0f}%)  Top-3: {stats['top3']:>2}/{stats['total']:<2} ({t3:3.0f}%)")

    if show_failures:
        failures = [(cat, f) for cat, stats in categories.items() for f in stats["failures"]]
        if failures:
            print(f"\n  Failures ({len(failures)}):")
            for cat, f in failures:
                print(f"    [{cat}] '{f['query']}' expected={f['expected']} got={f['got']}")


def evaluate(use_vector=False, hand_only=False):
    """Evaluate search quality. Reports hand and auto separately.

    Hand queries are the authoritative measure.
    Auto queries (graph-derived) serve as a consistency check — if they drop,
    the graph edges may have drifted.
    """
    mode = "BM25 + Vector" if use_vector else "BM25-only"

    # ── Hand-crafted queries (authoritative) ──
    hand_queries = _load_queries(HAND_FILE)
    t1_h, t3_h, tot_h, cats_h = _eval_set(hand_queries, "Hand-Crafted Queries", use_vector)

    # ── Auto-generated queries (consistency check) ──
    auto_queries = []
    if not hand_only:
        auto_queries = _load_queries(AUTO_FILE)
    t1_a, t3_a, tot_a, cats_a = _eval_set(auto_queries, "Auto-Generated (Graph Consistency)", use_vector)

    # ── Print ──
    print(f"\n{'#'*60}")
    print(f"  LAMMPS-CMD Evaluation ({mode})")
    print(f"{'#'*60}")

    _print_set_report("Hand-Crafted Queries  (authoritative)", t1_h, t3_h, tot_h, cats_h)
    if not hand_only and auto_queries:
        _print_set_report("Auto-Generated (Graph Consistency Check)", t1_a, t3_a, tot_a, cats_a, show_failures=False)

    # ── Combined summary ──
    if not hand_only and auto_queries:
        combined_t1 = t1_h + t1_a
        combined_t3 = t3_h + t3_a
        combined_tot = tot_h + tot_a
        print(f"\n{'='*60}")
        print(f"  Combined")
        print(f"{'='*60}")
        print(f"  Top-1:  {combined_t1}/{combined_tot} = {combined_t1/combined_tot*100:.0f}%")
        print(f"  Top-3:  {combined_t3}/{combined_tot} = {combined_t3/combined_tot*100:.0f}%")
        print(f"  (Hand {t3_h/tot_h*100:.0f}%  +  Auto {t3_a/tot_a*100:.0f}%  →  Combined {combined_t3/combined_tot*100:.0f}%)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--vector", action="store_true", help="Enable vector semantic search")
    ap.add_argument("--hand-only", action="store_true", help="Evaluate hand-crafted queries only")
    args = ap.parse_args()
    evaluate(use_vector=args.vector, hand_only=args.hand_only)
