#!/usr/bin/env python3
"""
LAMMPS command search — agent skill script.
Self-contained: reads graph_data.json, no server needed.

Usage:
  python search_lammps.py search "fix nvt" --limit 5
  python search_lammps.py detail fix_nh
  python search_lammps.py neighbors fix_nh
"""
import argparse, json, math, os, re, sys
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# graph_data.json is in the project root (2 levels up from scripts/)
DATA_FILE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "..", "graph_data.json"))

_data = None

def load_data():
    global _data
    if _data is None:
        with open(DATA_FILE, encoding="utf-8") as f:
            _data = json.load(f)
    return _data


# ═══════════════════════════════════════════════════════════════════
# BM25 + Graph search (same as search.html, but CLI)
# ═══════════════════════════════════════════════════════════════════

STOP = {"the","is","are","be","a","an","of","in","on","at","to","for","and","or",
        "with","can","do","does","will","not","no","this","that","it","its","by","as","if","all","also"}

def tokenize(s):
    return [t for t in re.findall(r"[a-z0-9]{2,}", s.lower()) if t not in STOP]

class LammpsSearch:
    def __init__(self):
        data = load_data()
        self.nodes = {n["id"]: n for n in data["nodes"]}
        self.edges = data["edges"]
        self.node_list = data["nodes"]

        # Build BM25 index
        self.docs = []
        self.doc_ids = []
        self.df = defaultdict(int)
        for n in self.node_list:
            text = f"{n['title']} {n.get('synopsis','')} {n.get('description','')} {n.get('syntax','')} " + \
                   " ".join(n.get("keywords", {}).keys() if isinstance(n.get("keywords"), dict) else [])
            tokens = tokenize(text)
            self.docs.append(tokens)
            self.doc_ids.append(n["id"])
            for t in set(tokens):
                self.df[t] += 1
        self.N = len(self.docs)
        self.doc_len = [len(d) for d in self.docs]
        self.avgdl = sum(self.doc_len) / max(1, self.N)

    def idf(self, term):
        n = self.df.get(term, 0)
        return math.log((self.N - n + 0.5) / (n + 0.5) + 1.0)

    def search(self, query, limit=10, phase=None):
        """BM25 text search + graph expansion."""
        toks = tokenize(query)
        if not toks:
            return [{"id": n["id"], "title": n["title"], "score": 0} for n in self.node_list[:limit]]

        idfs = {t: self.idf(t) for t in toks}
        scored = {}
        for i, (doc, nid) in enumerate(zip(self.docs, self.doc_ids)):
            s = 0
            for t in toks:
                if t not in self.df: continue
                tf = doc.count(t)
                num = tf * 2.5
                den = tf + 1.5 * (1 - 0.75 + 0.75 * self.doc_len[i] / self.avgdl)
                s += idfs[t] * num / den
            # Title boost
            title_toks = tokenize(self.nodes[nid]["title"])
            if sum(1 for t in toks if t in title_toks):
                s *= 1.3
            if s > 0:
                scored[nid] = s

        # Graph expansion
        boost_map = defaultdict(lambda: {"score": 0, "rel": set()})
        for nid, s in scored.items():
            for e in self.edges:
                if e["from"] == nid or e["to"] == nid:
                    other = e["to"] if e["from"] == nid else e["from"]
                    w = e.get("weight", 2)
                    boost_map[other]["score"] += s * w / 100
                    boost_map[other]["rel"].add(e["type"])

        for nid, info in boost_map.items():
            if nid in scored:
                scored[nid] += info["score"]
            elif phase is None or self.nodes.get(nid, {}).get("phase") == phase:
                scored[nid] = info["score"]

        # Sort and format
        results = []
        for nid, s in sorted(scored.items(), key=lambda x: -x[1])[:limit]:
            n = self.nodes[nid]
            rel = boost_map.get(nid, {}).get("rel", set())
            rel_types = list(rel) if nid not in {k for k, _ in scored.items() if _ == s} else []
            results.append({
                "id": nid, "title": n["title"], "phase": n["phase"],
                "synopsis": n.get("synopsis", ""),
                "score": round(s, 2),
                "relationships": rel_types,
                "url": n.get("url", ""),
            })
        return results

    def detail(self, cmd_id):
        """Full structured data for a command."""
        n = self.nodes.get(cmd_id)
        if not n: return {"error": f"Command '{cmd_id}' not found"}
        related = []
        for e in self.edges:
            if e["from"] == cmd_id or e["to"] == cmd_id:
                other_id = e["to"] if e["from"] == cmd_id else e["from"]
                related.append({
                    "node": other_id,
                    "type": e["type"],
                    "weight": e.get("weight", 0),
                    "source": e.get("source", ""),
                })
        related.sort(key=lambda x: -x["weight"])
        return {
            "id": n["id"], "title": n["title"], "phase": n["phase"],
            "synopsis": n.get("synopsis", ""),
            "description": n.get("description", ""),
            "syntax": n.get("syntax", ""),
            "keywords": n.get("keywords", {}),
            "examples": n.get("examples", []),
            "restrictions": n.get("restrictions", ""),
            "relationships": related,
            "url": n.get("url", ""),
        }

    def neighbors(self, cmd_id):
        """List all neighbors grouped by edge type."""
        n = self.nodes.get(cmd_id)
        if not n: return {"error": f"Command '{cmd_id}' not found"}
        groups = defaultdict(list)
        for e in self.edges:
            if e["from"] == cmd_id or e["to"] == cmd_id:
                other_id = e["to"] if e["from"] == cmd_id else e["from"]
                other = self.nodes.get(other_id, {})
                groups[e["type"]].append({
                    "id": other_id,
                    "title": other.get("title", other_id),
                    "weight": e.get("weight", 0),
                    "source": e.get("source", ""),
                })
        # Sort each group by weight
        for g in groups.values():
            g.sort(key=lambda x: -x["weight"])
        return {"id": cmd_id, "title": n["title"], "neighbors": dict(groups)}


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    p = argparse.ArgumentParser(prog="search_lammps.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("search")
    sp.add_argument("query")
    sp.add_argument("--limit", type=int, default=10)
    sp.add_argument("--phase", default=None)
    sp.add_argument("--verbose", "-v", action="store_true")
    sp.set_defaults(func=lambda args: print(json.dumps(
        LammpsSearch().search(args.query, args.limit, args.phase), indent=2, ensure_ascii=False)))

    dp = sub.add_parser("detail")
    dp.add_argument("cmd_id")
    dp.set_defaults(func=lambda args: print(json.dumps(
        LammpsSearch().detail(args.cmd_id), indent=2, ensure_ascii=False)))

    np = sub.add_parser("neighbors")
    np.add_argument("cmd_id")
    np.set_defaults(func=lambda args: print(json.dumps(
        LammpsSearch().neighbors(args.cmd_id), indent=2, ensure_ascii=False)))

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
