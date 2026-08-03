"""
LLM-based edge extraction for isolated nodes in the LAMMPS knowledge graph.

For each isolated node:
  1. Read local markdown (or fetch live from docs.lammps.org if stub)
  2. Ask DeepSeek to identify relationships with other graph nodes
  3. Add confirmed edges to graph_data_full.json

Usage:
  python fix_isolated_llm.py --api-key sk-xxx        # process all isolated
  python fix_isolated_llm.py --api-key sk-xxx --dry-run  # preview only
  python fix_isolated_llm.py --api-key sk-xxx --limit 10  # first 10
"""
import json, sys, os, re, time, argparse
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent
KB_DIR = ROOT / "lammps_kb"
GRAPH_FILE = ROOT / "graph_data_full.json"

# ── Fetch live page ──
def fetch_live_page(page_id):
    """Fetch the live HTML from docs.lammps.org and extract text content."""
    import urllib.request
    url = f"https://docs.lammps.org/{page_id}.html"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LAMMPS-KB/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  WARN: fetch failed for {page_id}: {e}")
        return None

    # Basic text extraction: strip HTML tags
    # Remove script/style/nav/footer
    for tag in ["script", "style", "nav", "footer", "head"]:
        html = re.sub(rf"<{tag}[^>]*>.*?</{tag}>", "", html, flags=re.DOTALL | re.IGNORECASE)

    # Get body content
    body = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
    if not body:
        return None
    text = body.group(1)

    # Strip all remaining HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse whitespace
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text[:4000] if len(text) > 4000 else text


def get_node_content(page_id, category):
    """Get content for a node: local file first, fall back to live fetch."""
    # Try local file
    candidates = list(KB_DIR.rglob(f"{page_id}.md"))
    if candidates:
        content = candidates[0].read_text(encoding="utf-8")
        # Check if stub (no Description section, very short)
        if "## Description" in content or len(content) > 500:
            return content
        print(f"  [{page_id}] local stub ({len(content)} chars), fetching live...")

    # Fetch live
    live = fetch_live_page(page_id)
    if live:
        return f"# Live page content from docs.lammps.org\n\n{live}"
    return None


def extract_edges_llm(page_id, node_title, content, all_node_ids, api_key):
    """Use LLM to find relationships between this isolated node and other graph nodes."""
    from llm_utils import call_llm_json

    # Trim content to fit token budget
    content_trimmed = content[:3000] if len(content) > 3000 else content

    # Build candidate list: all non-isolated command nodes (filter to likely relevant)
    # Focus on fix_, compute_, pair_, etc. — skip howto and general meta-pages
    candidates = sorted(
        nid for nid in all_node_ids
        if not nid.startswith("Howto_")
        and not nid.startswith("atc_")
        and nid not in {"angles", "computes", "dihedrals", "dumps", "fixes", "impropers",
                        "accel_styles", "commands_list", "echo", "log", "search",
                        "lepton_expression"}
        and nid != page_id
    )
    # If too many candidates, sample representative ones
    candidate_str = ", ".join(candidates[:200])
    if len(candidates) > 200:
        candidate_str += f" ... and {len(candidates) - 200} more (not shown, use your knowledge)"

    prompt = f"""You are a LAMMPS documentation expert. Analyze this page and identify which LAMMPS commands it is related to.

## Page: {page_id} — {node_title}

```
{content_trimmed}
```

## Candidate commands in the knowledge graph:
{candidate_str}

## Task
Find commands from the candidate list (or other well-known LAMMPS commands) that have a clear relationship with {page_id}. Return a JSON array of edges.

Each edge: {{"to": "command_id", "type": "...", "reason": "one sentence"}}

Edge types:
- "requires": {page_id} REQUIRES that command to work
- "creates": {page_id} internally creates/uses that command
- "alternative": {page_id} is an alternative to / can replace that command
- "related": {page_id} is related to / commonly used with that command
- "refers_to": {page_id} mentions/references that command

Rules:
- Only include relationships clearly stated or strongly implied in the content
- Command IDs must be lowercase_underscore (e.g., fix_nve, compute_temp)
- Return [] (empty array) if no clear relationships found
- Output ONLY the JSON array, nothing else"""

    try:
        edges = call_llm_json(
            prompt,
            system="You output only valid JSON arrays. No explanation.",
            api_key=api_key,
            max_tokens=600,
        )
        if not isinstance(edges, list):
            return []
        # Validate and clean
        valid = []
        for e in edges:
            if not isinstance(e, dict):
                continue
            target = e.get("to", "").strip()
            etype = e.get("type", "related")
            if target and target != page_id and etype in ("requires", "creates", "alternative", "related", "refers_to"):
                valid.append({
                    "to": target,
                    "type": etype,
                    "reason": e.get("reason", "")[:200],
                })
        return valid
    except Exception as e:
        print(f"  LLM error for {page_id}: {e}")
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", required=True, help="DeepSeek API key")
    ap.add_argument("--dry-run", action="store_true", help="Preview only, don't save")
    ap.add_argument("--limit", type=int, default=0, help="Max nodes to process")
    args = ap.parse_args()

    # Load graph
    with open(GRAPH_FILE, encoding="utf-8") as f:
        g = json.load(f)

    nodes = {n["id"]: n for n in g["nodes"]}
    all_ids = set(nodes.keys())

    # Find isolated nodes
    connected = set()
    for e in g["edges"]:
        connected.add(e["from"])
        connected.add(e["to"])
    isolated = sorted(all_ids - connected)

    print(f"Graph: {len(all_ids)} nodes, {len(g['edges'])} edges, {len(isolated)} isolated")

    # Separate into fixable vs unfixable
    # Skip: style index pages (they're not commands)
    skip = {"angles", "computes", "dihedrals", "dumps", "fixes", "impropers",
            "accel_styles", "commands_list", "echo", "log", "search", "lepton_expression"}
    targets = [(nid, nodes[nid]) for nid in isolated if nid not in skip]

    if args.limit:
        targets = targets[:args.limit]

    print(f"Processing {len(targets)} nodes (skipped {len(skip & set(isolated))} style-index pages)")
    print(f"{'DRY RUN — ' if args.dry_run else ''}API key: ...{args.api_key[-8:]}")
    print()

    # Edge type → weight mapping
    type_weight = {"requires": 10, "creates": 7, "alternative": 5, "related": 3, "refers_to": 2}
    existing_edges = {(e["from"], e["to"]) for e in g["edges"]}
    total_new = 0
    stats = {"found": 0, "empty": 0, "no_content": 0, "error": 0}
    all_new_edges = []

    for i, (nid, node) in enumerate(targets):
        cat = node.get("category", "?")
        title = node.get("title", nid)
        print(f"[{i+1}/{len(targets)}] {nid} ({cat}) — {title[:60]}")

        content = get_node_content(nid, cat)
        if not content:
            print(f"  -> no content available, skipping")
            stats["no_content"] += 1
            continue

        llm_edges = extract_edges_llm(nid, title, content, all_ids, args.api_key)

        if not llm_edges:
            print(f"  -> no relationships found")
            stats["empty"] += 1
        else:
            # Filter: only keep edges to nodes that exist in the graph
            new_for_node = []
            for e in llm_edges:
                target = e["to"]
                if target not in all_ids:
                    # Try fuzzy: maybe the LLM returned the right ID with different formatting
                    continue
                if target == nid:
                    continue
                key = (nid, target)
                if key in existing_edges or (target, nid) in existing_edges:
                    continue  # already exists
                etype = e["type"]
                edge = {
                    "from": nid,
                    "to": target,
                    "type": etype,
                    "weight": type_weight.get(etype, 3),
                    "source": f"LLM post-hoc: {e.get('reason', '')}",
                    "source_type": "llm_posthoc",
                    "confidence": "medium",
                }
                new_for_node.append(edge)
                existing_edges.add(key)
                existing_edges.add((target, nid))  # prevent reverse too

            if new_for_node:
                print(f"  -> {len(new_for_node)} new edges:")
                for e in new_for_node:
                    print(f"     {e['from']} --[{e['type']}]--> {e['to']}  ({e.get('source','')[:80]})")
                all_new_edges.extend(new_for_node)
                total_new += len(new_for_node)
                stats["found"] += 1
            else:
                print(f"  -> {len(llm_edges)} suggested but all already exist or invalid targets")
                stats["empty"] += 1

        # Rate limit
        if i < len(targets) - 1:
            time.sleep(0.3)

    print()
    print("=" * 60)
    print(f"Summary: {stats['found']} nodes got edges, {stats['empty']} none found, "
          f"{stats['no_content']} no content, {stats['error']} errors")
    print(f"Total new edges: {total_new}")

    if total_new > 0 and not args.dry_run:
        g["edges"].extend(all_new_edges)
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(g, f, ensure_ascii=False, indent=2)

        # Re-count isolated
        connected2 = set()
        for e in g["edges"]:
            connected2.add(e["from"]); connected2.add(e["to"])
        new_isolated = len(all_ids - connected2)
        print(f"Isolated: {len(isolated)} -> {new_isolated}")
        print(f"Saved to {GRAPH_FILE}")
    elif args.dry_run:
        print("DRY RUN — not saved. Remove --dry-run to apply.")


if __name__ == "__main__":
    main()
