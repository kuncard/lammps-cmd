"""
Build full LAMMPS knowledge graph from scraped markdown files.
Extracts nodes (command pages) and edges (Related commands + Restrictions rules).

Usage: python build_full_graph.py
Output: graph_data.json (full graph)
"""
import json, re, time, sys, os, argparse
from pathlib import Path
from collections import defaultdict

from logging_setup import setup_logging
log = setup_logging(__name__)

ROOT = Path(__file__).parent
KB_DIR = ROOT / "lammps_kb"

# Map LAMMPS command category → phase-like group for visualization
CATEGORY_PHASE = {
    "general": "init",
    "fix": "integ",
    "compute": "compute",
    "pair": "force",
    "bond": "force",
    "angle": "force",
    "dihedral": "force",
    "improper": "force",
    "kspace": "force",
    "dump": "output",
    "howto": "guide",
    "root": "init",
}

def parse_frontmatter(md_text):
    """Extract YAML frontmatter."""
    fm = {}
    m = re.match(r"^---\n(.*?)\n---", md_text, re.DOTALL)
    if m:
        for line in m.group(1).strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
    return fm

def extract_related_edges(page_id, md_text):
    """Rule A: Parse 'Related Commands' section for explicit cross-references."""
    edges = []
    # Find the Related Commands section
    sec = re.search(r"## Related Commands\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    if not sec:
        return edges

    # Extract markdown links: - [text](href.html)
    links = re.findall(r"\[([^\]]+)\]\(([^)]+\.html)\)", sec.group(1))
    for label, href in links:
        target_id = href.replace(".html","").split("#")[0]
        if target_id and target_id != page_id:
            edges.append({
                "from": page_id, "to": target_id,
                "type": "related", "weight": 2,
                "source": f"Related commands: {label.strip()}"
            })
    return edges

def extract_restriction_edges(page_id, md_text):
    """Rule B: Parse 'Restrictions' section for implicit constraints."""
    edges = []
    sec = re.search(r"## Restrictions\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    if not sec:
        return edges

    restrict = sec.group(1)

    patterns = [
        # "must be after X" / "must come after X"
        (r"must\s+(?:come\s+)?(?:be\s+)?after\s+(?:the\s+)?([\w][\w\s,]+?)(?:\.|,|\s+(?:command|fix|compute)|$)", "requires", 10),
        # "requires X" / "needs X to be set"
        (r"(?:requires|needs)\s+(?:a\s+|the\s+)?([\w][\w\s,]+?)(?:\s+to\s+be\s+set|\s+command|\s+fix|\s+compute|\.|,|\s+(?:and|or|before|first|prior)|$)", "requires", 10),
        # "cannot be used with X"
        (r"cannot\s+(?:be\s+)?used\s+(?:with|after|before)\s+([\w][\w\s,]+?)(?:\.|,|\s+(?:command|fix|compute)|$)", "incompatible", 8),
        # "must not be combined with X" / "should not be combined with X"
        (r"(?:must|should)\s+not\s+(?:be\s+)?(?:combined|used)\s+with\s+([\w][\w\s,]+?)(?:\.|,|$)", "incompatible", 8),
        # "do NOT use with X" / "do not use X"
        (r"do\s+[nN][oO][tT]\s+use\s+(?:with\s+)?(?:another\s+)?([\w][\w\s,]+?)(?:\.|,|\s+(?:command|fix|compute|style)|$)", "incompatible", 8),
        # "X must be defined before" / "X must be set before"
        (r"(\w[\w_]*(?:\s+\w[\w_]*){0,3})\s+must\s+be\s+(?:defined|set|specified)\s+before", "requires", 10),
        # "internally creates a X compute" / "creates a X compute"
        (r"(?:internally\s+)?creates\s+(?:a|an)\s+([\w][\w\s,]+?)(?:\s+(?:compute|fix)|\.|,|$)", "creates", 7),
    ]

    for pattern, etype, weight in patterns:
        matches = re.findall(pattern, restrict, re.IGNORECASE)
        for m_text in matches:
            # Extract command-like names from matched text
            cmds = re.findall(r"[a-z_]{3,}", m_text.strip().lower())
            for cmd in cmds:
                # Filter out non-command words
                if cmd in {"and","the","for","not","any","all","its","set","use","used","with","after","this","same","must","that","from","only","also","such","each","both","more","than","very","into","over","under","well","here","there"}:
                    continue
                if cmd != page_id:
                    edges.append({
                        "from": page_id, "to": cmd,
                        "type": etype, "weight": weight,
                        "source": f"Restrictions: {m_text.strip()[:100]}"
                    })
    return edges

def build_graph(api_key=None, llm_limit=0):
    """Walk lammps_kb/ and build the full graph."""
    nodes = []
    edges = []
    seen_edges = set()
    category_counts = defaultdict(int)
    llm_count = 0

    # Walk all md files (both flat and in subdirectories)
    for md_path in sorted(KB_DIR.rglob("*.md")):
        if md_path.name == "manifest.json":
            continue
        if "index" in md_path.name.lower():
            continue

        with open(md_path, encoding="utf-8") as f:
            md_text = f.read()

        fm = parse_frontmatter(md_text)
        page_id = fm.get("id", md_path.stem)
        title = fm.get("title", page_id)
        url = fm.get("url", "")

        # Determine category from directory
        rel = md_path.relative_to(KB_DIR)
        category = str(rel.parent) if rel.parent != Path(".") else "root"

        # Extract synopsis (first line after frontmatter heading)
        synopsis = ""
        lines = md_text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("# ") and i < 10:
                synopsis = line.lstrip("# ").strip()
                break

        # Add node (skip if already added from a preferred category)
        existing = [n for n in nodes if n["id"] == page_id]
        if existing:
            # Keep the one with more specific category (not "root")
            if category != "root" and existing[0].get("category") == "root":
                nodes.remove(existing[0])
                category_counts["root"] -= 1
            else:
                continue

        phase = CATEGORY_PHASE.get(category, "init")
        nodes.append({
            "id": page_id,
            "title": title,
            "phase": phase,
            "category": category,
            "synopsis": synopsis,
            "url": url,
        })
        category_counts[category] += 1

        # Extract edges
        rel_edges = extract_related_edges(page_id, md_text)
        restr_edges = extract_restriction_edges(page_id, md_text)
        llm_edges = []

        if api_key and (llm_limit == 0 or llm_count < llm_limit):
            llm_edges = extract_llm_edges(page_id, md_text, api_key)
            llm_count += 1
            if llm_count % 10 == 0:
                log.info("  LLM processed %s pages...", llm_count)

        # ── Cross-validation: merge edges from all 3 sources ──
        for e in rel_edges:
            e["source_type"] = "rule_related"
            e["confidence"] = "high"
            key = (e["from"], e["to"], e["type"])
            if key not in seen_edges: seen_edges.add(key); edges.append(e)

        for e in restr_edges:
            e["source_type"] = "rule_restrictions"
            e["confidence"] = "high"
            key = (e["from"], e["to"], e["type"])
            if key not in seen_edges: seen_edges.add(key); edges.append(e)

        for e in llm_edges:
            e["source_type"] = "llm_only"
            e["confidence"] = "medium"
            key = (e["from"], e["to"], e["type"])
            if key in seen_edges:
                # Edge confirmed by both rule and LLM → boost
                existing = next(x for x in edges if (x["from"],x["to"],x["type"])==key)
                existing["confidence"] = "high"
                existing["source_type"] = "rule_and_llm"
                existing["weight"] = max(existing["weight"], e["weight"])
                continue
            seen_edges.add(key); edges.append(e)

    # ── Implicit parent-child edges ──
    # Connect atc_* sub-commands to fix_atc (all scraped from same page)
    if any(n["id"] == "fix_atc" for n in nodes):
        atc_kids = sorted(n["id"] for n in nodes if n["id"].startswith("atc_") and n["id"] != "fix_atc")
        for kid in atc_kids:
            for fwd, rev in [("fix_atc", kid), (kid, "fix_atc")]:
                key = (fwd, rev, "related")
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append({
                        "from": fwd, "to": rev,
                        "type": "related", "weight": 5,
                        "source": "implicit: parent-child",
                        "source_type": "implicit_parent",
                        "confidence": "high",
                    })
        if atc_kids:
            log.info("  Added %d implicit parent-child edges for fix_atc", len(atc_kids) * 2)

    # NOTE: After rebuilding the graph, run fix_isolated_llm.py to add edges for
    # HowTo guides and other nodes the rule-based extractor can't handle.
    # The scraper currently produces stubs for HowTo pages (missing Description section),
    # so LLM extraction in build_graph() returns empty for those nodes.
    # fix_isolated_llm.py fetches live page content and uses LLM to find relationships.

    # ── Dedup: keep best (from,to) pair, prefer highest confidence + weight ──
    conf_rank = {"high": 3, "medium": 2, "low": 1}
    best_edge = {}
    for e in edges:
        pair = (e["from"], e["to"])
        if pair not in best_edge:
            best_edge[pair] = e
        else:
            cur = best_edge[pair]
            e_conf = conf_rank.get(e.get("confidence","low"), 0)
            cur_conf = conf_rank.get(cur.get("confidence","low"), 0)
            if e_conf > cur_conf or (e_conf == cur_conf and e.get("weight",0) > cur.get("weight",0)):
                best_edge[pair] = e

    final_edges = list(best_edge.values())

    # ── Filter self-loops and invalid edges ──
    node_ids = {n["id"] for n in nodes}
    final_edges = [e for e in final_edges
                   if e["from"] in node_ids and e["to"] in node_ids
                   and e["from"] != e["to"]]

    log.info("Nodes: %s  Edges: %s", len(nodes), len(final_edges))
    for cat, count in sorted(category_counts.items()):
        log.info("  %s: %s nodes", cat, count)

    # Edge type stats
    type_counts = defaultdict(int)
    conf_counts = defaultdict(int)
    source_counts = defaultdict(int)
    for e in final_edges:
        type_counts[e["type"]] += 1
        conf_counts[e.get("confidence","low")] += 1
        source_counts[e.get("source_type","unknown")] += 1
    log.info("Edges by type:")
    for t, c in sorted(type_counts.items()):
        log.info("  %s: %s", t, c)
    log.info("Edges by confidence:")
    for c, n in sorted(conf_counts.items()):
        log.info("  %s: %s", c, n)
    log.info("Edges by source:")
    for s, n in sorted(source_counts.items()):
        log.info("  %s: %s", s, n)

    return {
        "nodes": nodes,
        "edges": final_edges,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "docs.lammps.org (scraped HTML)",
    }

# ── LLM Edge Extraction ──
from llm_utils import call_llm_json


def extract_llm_edges(page_id, md_text, api_key):
    """Rule C: Use LLM to extract implicit edges from Description text."""

    # Extract description section
    desc_match = re.search(r"## Description\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    if not desc_match:
        return []
    description = desc_match.group(1)[:2000]

    # Also get related commands as hints
    related_match = re.search(r"## Related Commands\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    related_hint = related_match.group(1)[:300] if related_match else "(none)"

    prompt = f"""You are a LAMMPS documentation analyst. Given a LAMMPS command page, extract the relationships between this command and other commands. This command ID is: {page_id}

Output ONLY valid JSON array. No explanation, no markdown fences.

Each edge: {{"from": "{page_id}", "to": "other_command_id", "type": "...", "source": "..."}}

Edge types:
- "requires": this command REQUIRES that command to be set first
- "creates": this command internally creates that command
- "incompatible": this command CANNOT be used with that command
- "alternative": alternative to / replaces that command

IMPORTANT RULES:
- Only include relationships clearly stated or strongly implied in the description
- Command IDs should be lowercase_underscore (e.g., fix_nve, compute_temp)
- Do NOT repeat relationships already listed in Related Commands: {related_hint}
- Output ONLY the JSON array, nothing else

## Description of {page_id}:

{description}"""

    try:
        edges = call_llm_json(
            prompt,
            system="You output only valid JSON arrays. No explanation.",
            api_key=api_key,
            max_tokens=500,
        )
        if not isinstance(edges, list):
            return []
        # Add weight and source
        for e in edges:
            e["source"] = f"LLM: {e.get('source', e.get('label', 'implicit'))}"
            e["weight"] = {"requires": 10, "incompatible": 8, "creates": 7, "alternative": 5}.get(e.get("type", ""), 3)
        return edges
    except Exception as e:
        log.warning("    LLM failed for %s: %s", page_id, e)
        return []


# ── LLM Edge Verification ──

def load_node_doc(page_id, kb_dir=KB_DIR):
    """Load the full markdown doc for a node, searching across subdirectories."""
    # Try exact filename match first
    candidates = list(kb_dir.rglob(f"{page_id}.md"))
    if not candidates:
        # Try case-insensitive
        candidates = [p for p in kb_dir.rglob("*.md") if p.stem.lower() == page_id.lower()]
    if not candidates:
        return None, None

    md_path = candidates[0]  # Use first match
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()

    # Extract Description section (the richest source of relationship info)
    desc_match = re.search(r"## Description\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    description = desc_match.group(1)[:1500].strip() if desc_match else ""

    # Also grab Restrictions if present
    restr_match = re.search(r"## Restrictions\n(.*?)(?=\n## |\Z)", md_text, re.DOTALL)
    restrictions = restr_match.group(1)[:500].strip() if restr_match else ""

    return description, restrictions


def verify_edge_with_llm(edge, kb_dir, api_key):
    """Ask LLM to verify a single edge by reading both nodes' documentation.

    Returns: {verdict: "confirmed"|"refuted"|"uncertain", reasoning: "...", weight_adjustment: int}
    """

    from_id = edge["from"]
    to_id = edge["to"]
    edge_type = edge.get("type", "related")
    edge_source = edge.get("source", "")[:200]

    from_desc, from_restr = load_node_doc(from_id, kb_dir)
    to_desc, to_restr = load_node_doc(to_id, kb_dir)

    if not from_desc and not to_desc:
        return {"verdict": "uncertain", "reasoning": "Could not load either document."}

    prompt = f"""You are a LAMMPS documentation expert. Verify whether the following relationship between two LAMMPS commands is CORRECT.

## Claimed Relationship
- **{from_id}** --[{edge_type}]--> **{to_id}**
- Original source: {edge_source}

## Documentation for `{from_id}`
{from_desc or "(no description found)"}
{f"### Restrictions: {from_restr}" if from_restr else ""}

## Documentation for `{to_id}`
{to_desc or "(no description found)"}
{f"### Restrictions: {to_restr}" if to_restr else ""}

## Task
Based ONLY on the documentation above, judge whether the claimed relationship is valid.

Output ONLY valid JSON:
{{"verdict": "confirmed"|"refuted"|"uncertain", "reasoning": "one-sentence evidence from the docs"}}

Rules:
- "confirmed": the docs explicitly state or strongly imply this relationship
- "refuted": the docs contradict this claim (e.g. "can be used with any X" refutes an incompatibility)
- "uncertain": the docs don't clearly confirm or refute
- Keep reasoning under 150 characters"""

    try:
        verdict = call_llm_json(
            prompt,
            system="You output only valid JSON. No explanation outside JSON.",
            api_key=api_key,
            max_tokens=200,
        )
        if not isinstance(verdict, dict):
            return {"verdict": "uncertain", "reasoning": "LLM returned non-dict response"}
        return {
            "verdict": verdict.get("verdict", "uncertain"),
            "reasoning": verdict.get("reasoning", ""),
        }
    except Exception as e:
        return {"verdict": "uncertain", "reasoning": f"LLM call failed: {str(e)[:80]}"}


def verify_edges(graph, api_key, verify_limit=0, kb_dir=KB_DIR):
    """Verify edges with LLM, in priority order.

    Priority (highest first):
      1. LLM-extracted edges (medium confidence, need verification)
      2. Rule-restriction edges (regex can have false positives)
      3. Rule-related edges with high weight (>=5)

    Returns updated graph with verification results merged into edges.
    """
    edges = graph["edges"]
    nodes_dict = {n["id"]: n for n in graph["nodes"]}

    # Sort by verification priority
    def priority(e):
        src = e.get("source_type", "")
        if src == "llm_only":
            return 0  # Highest priority
        elif src == "rule_restrictions":
            return 1
        elif e.get("weight", 0) >= 5:
            return 2
        else:
            return 3  # Low-weight related edges — skip unless --verify-all

    # Filter: keep edges that have both nodes in the KB
    verifiable = []
    skipped_missing = 0
    for e in edges:
        from_id = e["from"]
        to_id = e["to"]
        from_doc = list(kb_dir.rglob(f"{from_id}.md"))
        to_doc = list(kb_dir.rglob(f"{to_id}.md"))
        if not from_doc:
            from_doc = [p for p in kb_dir.rglob("*.md") if p.stem.lower() == from_id.lower()]
        if not to_doc:
            to_doc = [p for p in kb_dir.rglob("*.md") if p.stem.lower() == to_id.lower()]
        if from_doc and to_doc:
            verifiable.append(e)
        else:
            skipped_missing += 1

    verifiable.sort(key=priority)

    if verify_limit > 0:
        verifiable = verifiable[:verify_limit]

    total = len(verifiable)
    log.info("=" * 60)
    log.info("LLM Edge Verification: %s edges to verify (%s skipped — missing docs)", total, skipped_missing)
    priority_labels = {0: "llm-extracted", 1: "rule-restriction", 2: "high-weight", 3: "low-weight"}
    pcounts = {}
    for e in verifiable:
        p = priority(e)
        pcounts[p] = pcounts.get(p, 0) + 1
    for p, c in sorted(pcounts.items()):
        log.info("  Priority %s (%s): %s edges", p, priority_labels.get(p, '?'), c)

    confirmed = 0
    refuted = 0
    uncertain = 0
    edge_index = {(e["from"], e["to"], e.get("type", "")): i for i, e in enumerate(edges)}

    for i, edge in enumerate(verifiable):
        vid = f"{edge['from']} -[{edge['type']}]-> {edge['to']}"
        result = verify_edge_with_llm(edge, kb_dir, api_key)

        # Merge verification into the original edge in the graph
        key = (edge["from"], edge["to"], edge.get("type", ""))
        if key in edge_index:
            orig = edges[edge_index[key]]
            orig["verified"] = True
            orig["verdict"] = result["verdict"]
            orig["verify_reasoning"] = result.get("reasoning", "")

            if result["verdict"] == "confirmed":
                confirmed += 1
                # Boost confidence
                if orig.get("confidence") == "medium":
                    orig["confidence"] = "high"
                    orig["source_type"] = orig.get("source_type", "") + "+verified"
                # Boost weight slightly for confirmed edges
                orig["weight"] = min(10, orig.get("weight", 1) + 1)
            elif result["verdict"] == "refuted":
                refuted += 1
                orig["confidence"] = "low"
                orig["weight"] = max(0, orig.get("weight", 1) - 4)
            else:
                uncertain += 1

        # Progress indicator
        if (i + 1) % 20 == 0 or i == total - 1:
            log.info("  [%s/%s] +%s -%s ~%s  (%s%%)", i + 1, total, confirmed, refuted, uncertain, 100 * (i + 1) // total)

    # Summary
    log.info("")
    log.info("Verification complete: +%s confirmed  -%s refuted  ~%s uncertain", confirmed, refuted, uncertain)
    if refuted > 0:
        refuted_edges = [e for e in edges if e.get("verdict") == "refuted"]
        log.warning("  Refuted edges (confidence->low, weight reduced):")
        for e in refuted_edges[:10]:
            log.warning("    %s -[%s]-> %s: %s", e['from'], e['type'], e['to'], e.get('verify_reasoning', '?')[:100])
        if len(refuted_edges) > 10:
            log.warning("    ... and %s more", len(refuted_edges) - 10)

    return graph


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="graph_data_full.json")
    ap.add_argument("--use-llm", action="store_true", help="Phase 1: LLM edge extraction (needs DEEPSEEK_API_KEY)")
    ap.add_argument("--llm-limit", type=int, default=0, help="Max pages for LLM extraction (0=all)")
    ap.add_argument("--verify", action="store_true", help="Phase 2: LLM edge verification (needs DEEPSEEK_API_KEY)")
    ap.add_argument("--verify-limit", type=int, default=0, help="Max edges to verify (0=all, prioritized)")
    args = ap.parse_args()

    need_api = args.use_llm or args.verify
    api_key = os.environ.get("DEEPSEEK_API_KEY", "") if need_api else None
    if need_api and not api_key:
        log.error("--use-llm / --verify requires DEEPSEEK_API_KEY env var")
        sys.exit(1)

    # Phase 1: Build graph (with optional LLM extraction)
    graph = build_graph(api_key=api_key, llm_limit=args.llm_limit if args.use_llm else 0)

    # Phase 2: LLM verification
    if args.verify:
        graph = verify_edges(graph, api_key, verify_limit=args.verify_limit)

    out_path = ROOT / args.output
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    log.info("Saved to %s (%.0f KB)", out_path, len(json.dumps(graph)) / 1024)
