#!/usr/bin/env python3
"""
Extract LAMMPS graph edges from documentation pages.

Three sources:
  1. EXPLICIT — Related commands + Restrictions ordering rules (from doc text)
  2. LLM-INFERRED — Description → LLM prompt → structured edges
  3. MERGED — Combine all sources, de-duplicate, mark confidence

Each edge has a `source` field: "related_cmd" | "restrictions" | "llm_v1"
"""

import json, os, re, sys, urllib.request

# DeepSeek API
LLM_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
LLM_URL = "https://api.deepseek.com/v1/chat/completions"

# ═══════════════════════════════════════════════════════════════════
# Source 1: EXPLICIT extraction from doc text
# ═══════════════════════════════════════════════════════════════════

def extract_explicit(page_id: str, page_data: dict) -> list[dict]:
    """
    Extract edges from:
    - related: explicit cross-references in doc
    - restrictions: "must be after", "requires", "cannot be used with"
    Returns list of {from, to, type, label, source}
    """
    edges = []

    # 1a. Related commands (explicit doc cross-references)
    for rel in page_data.get("related", []):
        target = rel.replace(" ", "_").lower().replace("/", "_")
        edges.append({
            "from": page_id, "to": target,
            "type": "related", "label": "",
            "source": "related_cmd"
        })

    # 1b. Restrictions parsing
    restrict = page_data.get("restrictions", "")
    # Pattern: "must come after X" / "must be defined before Y"
    patterns = [
        (r"must\s+(?:come\s+)?(?:be\s+)?after\s+(?:the\s+)?(\w[\w\s,]+?)(?:\.|,|\s+by)", "requires", "must be after"),
        (r"(?:requires|needs)\s+(?:a\s+|the\s+)?(\w[\w\s,]+?)(?:\s+to\s+be\s+set|\s+command|\s+fix|\s+compute|\.|,|\s+by)", "requires", "requires"),
        (r"cannot\s+(?:be\s+)?used\s+(?:with|after|before)\s+(\w[\w\s,]+?)(?:\.|,)", "alternative", "cannot use with"),
        (r"(?:must|should)\s+not\s+(?:be\s+)?combined\s+with\s+(\w[\w\s,]+?)(?:\.|,)", "alternative", "do not combine"),
    ]

    for pattern, etype, label in patterns:
        matches = re.findall(pattern, restrict, re.IGNORECASE)
        for m in matches:
            # Extract command names from matched text
            cmds = re.findall(r"[a-z_]+", m.strip().lower())
            for cmd in cmds:
                if len(cmd) >= 3:
                    edges.append({
                        "from": page_id, "to": cmd,
                        "type": etype, "label": label,
                        "source": "restrictions"
                    })

    return edges


# ═══════════════════════════════════════════════════════════════════
# Source 2: LLM prompt for implicit relationships
# ═══════════════════════════════════════════════════════════════════

LLM_SYSTEM_PROMPT = """You are a LAMMPS documentation analyst. Given a LAMMPS command page, extract
the relationships between this command and other commands.

Output ONLY valid JSON array. No explanation, no markdown fences.

Each edge: {"from": "this_page_id", "to": "other_command_id", "type": "...", "label": "..."}

Edge types:
- "requires": this command REQUIRES that command to be set first (input script ordering)
  Example: read_data requires units to be set before it
- "creates": this command automatically/interally creates the other command
  Example: fix nvt internally creates compute temp and compute pressure
- "alternative": this command is an alternative to / replaces that command
  Example: fix nvt is an alternative to fix nve for thermostatting
- "used_with": this command is commonly used together with that command
  Example: fix langevin is commonly used WITH fix nve

Only include relationships that are EXPLICITLY stated or CLEARLY implied in the description.
Do not guess. If unsure, omit the edge.
Command IDs should be lowercase with underscores (e.g., "fix_nve", "compute_temp", "thermo_style").
"""

def build_llm_prompt(page_id: str, page_data: dict) -> str:
    """Build an LLM prompt to extract implicit edges from a command page."""
    return f"""Analyze this LAMMPS command page and extract relationships.

Page ID: {page_id}
Title: {page_data.get('title', '')}
Category: {page_data.get('type', '')}

Description:
{page_data.get('description', '')[:2000]}

Related commands (explicit from docs): {', '.join(page_data.get('related', []))}

Return JSON array of edges. Example:
[{{"from": "{page_id}", "to": "fix_nve", "type": "alternative", "label": "thermostat choice"}},
 {{"from": "{page_id}", "to": "compute_temp", "type": "creates", "label": "internal compute"}}]

Only edges not already covered by the Related commands list above.
If you see no additional relationships, return []."""


# ═══════════════════════════════════════════════════════════════════
# Demo: run on a few pages and compare
# ═══════════════════════════════════════════════════════════════════

DEMO_PAGES = {
    "fix_nh": {
        "title": "fix nvt / fix npt / fix nph",
        "type": "fix",
        "description": """These commands perform time integration on Nose-Hoover style
non-Hamiltonian equations. The thermostat is applied to only the translational degrees of
freedom for the particles. The barostat is coupled to the box dimensions. These fixes
perform BOTH thermostatting/barostatting AND time integration — do not use another time
integration fix (like fix nve) on the same atoms. A temperature compute (fix_ID_temp) and
pressure compute (fix_ID_press) are created internally as if these commands were issued:
compute fix-ID_temp group-ID temp
compute fix-ID_press group-ID pressure fix-ID_temp""",
        "related": ["fix nve", "fix_modify", "run_style"],
        "restrictions": "x, y, z cannot be barostatted if the associated dimension is not periodic. Tstop cannot be 0.0.",
    },
    "fix_langevin": {
        "title": "fix langevin",
        "type": "fix",
        "description": """Apply a Langevin thermostat. Total force = F_conservative + F_friction
+ F_random. This fix does NOT perform time integration — it only modifies forces to
thermostat. Thus you must use another time integration fix (like fix nve) on the same atoms.
Should not normally be used with other thermostatting fixes. The gjf keyword has been
removed — use fix gjf instead.""",
        "related": ["fix nvt", "fix temp/rescale", "fix viscous", "fix gjf", "fix gle", "fix gld"],
        "restrictions": "None.",
    },
    "velocity": {
        "title": "velocity",
        "type": "command",
        "description": """Set or change the velocities of a group of atoms. The create style
generates an ensemble of velocities using a random number generator at the specified
temperature. The set style assigns velocities. The scale style rescales to the specified
temperature. For rigid bodies, do 'run 0' then 'velocity all scale T' to fix initial
velocities after SHAKE constraints are applied.""",
        "related": ["fix rigid", "fix shake", "lattice"],
        "restrictions": "Assigning temperature via 'create' to systems with rigid bodies or SHAKE constraints may not work as expected.",
    },
    "timestep": {
        "title": "timestep",
        "type": "command",
        "description": """Set the timestep size for subsequent molecular dynamics simulations.
The default value depends on the units command. When using run_style respa, dt is the
timestep for the outer loop.""",
        "related": ["fix dt/reset", "run", "run_style respa", "units"],
        "restrictions": "None.",
    },
    "run": {
        "title": "run",
        "type": "command",
        "description": """Run or continue dynamics for a specified number of timesteps.
When using run_style respa, N refers to outer loop timesteps. The upto keyword starts
from the current timestep and runs until reaching N. The start/stop keywords allow fixes
that change values over time to ramp across multiple runs. The every keyword breaks the
run into segments.""",
        "related": ["minimize", "run_style", "temper", "fix halt"],
        "restrictions": "Without upto, N must fit in a signed 32-bit integer.",
    },
    "thermo_style": {
        "title": "thermo_style",
        "type": "command",
        "description": """Set the style and content of thermodynamic output. Style one is a
single line. Style multi provides multi-line output with labels. Style custom allows any
combination of keywords. This command must come after the simulation box is defined.
Uses internal computes thermo_temp, thermo_press, and thermo_pe by default.""",
        "related": ["thermo", "thermo_modify", "fix_modify", "compute temp", "compute pressure"],
        "restrictions": "This command must come after the simulation box is defined by a read_data, read_restart, or create_box command.",
    },
}


def run_extraction(pages: dict, save_to: str = None):
    """Run extraction pipeline and output comparison."""
    all_edges = []
    stats = {"related_cmd": 0, "restrictions": 0, "llm_v1": 0, "total": 0}

    print("=" * 60)
    print("LAMMPS Graph Edge Extraction Pipeline")
    print("=" * 60)

    for pid, pdata in pages.items():
        print(f"\n── {pid} ({pdata['title']}) ──")

        # Step 1: Explicit
        explicit = extract_explicit(pid, pdata)
        stats["related_cmd"] += sum(1 for e in explicit if e["source"] == "related_cmd")
        stats["restrictions"] += sum(1 for e in explicit if e["source"] == "restrictions")

        print(f"  Related cmd edges: {sum(1 for e in explicit if e['source']=='related_cmd')}")
        for e in explicit:
            if e["source"] == "related_cmd":
                print(f"    → {e['to']} [{e['type']}]")

        print(f"  Restrictions edges: {sum(1 for e in explicit if e['source']=='restrictions')}")
        for e in explicit:
            if e["source"] == "restrictions":
                print(f"    → {e['to']} [{e['type']}] ({e['label']})")

        all_edges.extend(explicit)

        # Step 2: Show LLM prompt (not calling LLM here — needs API key)
        prompt = build_llm_prompt(pid, pdata)
        print(f"  LLM prompt ready: {len(prompt)} chars (needs API call)")

    stats["total"] = len(all_edges)

    print(f"\n{'=' * 60}")
    print(f"SUMMARY: {stats['total']} edges extracted from {len(pages)} pages")
    print(f"  related_cmd: {stats['related_cmd']}")
    print(f"  restrictions: {stats['restrictions']}")
    print(f"  llm_v1: {stats['llm_v1']} (pending LLM calls)")
    print(f"\nLLM prompt format ready. Run with --llm to invoke LLM extraction.")


# ═══════════════════════════════════════════════════════════════════
# Comparison: extracted vs hand-written
# ═══════════════════════════════════════════════════════════════════

def compare_with_handwritten():
    """Compare extracted edges with the hand-written ones in build_lammps_graph.py"""
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        from build_lammps_graph import EDGES as HW_EDGES, NODES
        hw_ids = {n["id"] for n in NODES}
        hw_edges = {(e["from"], e["to"], e["type"]) for e in HW_EDGES if e["from"] in DEMO_PAGES or e["to"] in DEMO_PAGES}

        print(f"\n{'=' * 60}")
        print("COMPARISON: Hand-written vs Doc-extracted")
        print("=" * 60)

        # Run extraction
        extracted = []
        for pid, pdata in DEMO_PAGES.items():
            extracted.extend(extract_explicit(pid, pdata))
        ext_set = {(e["from"], e["to"], e["type"]) for e in extracted}

        # Both
        both = hw_edges & ext_set
        hw_only = hw_edges - ext_set
        ext_only = ext_set - hw_edges

        print(f"\n  Both (agreement): {len(both)}")
        for f, t, tp in sorted(both):
            print(f"    {f} -> {t} [{tp}]")

        print(f"\n  Hand-written only (my guess): {len(hw_only)}")
        for f, t, tp in sorted(hw_only):
            print(f"    {f} -> {t} [{tp}] (needs verification)")

        print(f"\n  Doc-extracted only (new): {len(ext_only)}")
        for f, t, tp in sorted(ext_only):
            print(f"    {f} -> {t} [{tp}]")

    except ImportError:
        print("build_lammps_graph.py not found, skipping comparison")


# ═══════════════════════════════════════════════════════════════════
# LLM invocation
# ═══════════════════════════════════════════════════════════════════

def call_llm(page_id: str, page_data: dict) -> list[dict]:
    """Call DeepSeek LLM to extract implicit edges from a command page."""
    prompt = build_llm_prompt(page_id, page_data)
    data = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": LLM_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 500,
        "temperature": 0.0,
    }).encode()

    try:
        req = urllib.request.Request(LLM_URL, data=data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_KEY}",
        })
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        text = resp["choices"][0]["message"]["content"].strip()

        # Parse JSON from response (handle markdown fences)
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        edges = json.loads(text)
        if isinstance(edges, list):
            for e in edges:
                e["source"] = "llm_v1"
            return edges
        return []
    except Exception as ex:
        print(f"  LLM error for {page_id}: {ex}", file=sys.stderr)
        return []


def run_llm_extraction(pages: dict, save_to: str = None):
    """Run LLM extraction on all pages and collect edges."""
    all_llm_edges = []
    stats = {"success": 0, "failed": 0, "edges": 0}

    print(f"\n{'=' * 60}")
    print("LLM EDGE EXTRACTION")
    print("=" * 60)

    for pid, pdata in pages.items():
        print(f"\n  [{pid}] ", end="", flush=True)
        edges = call_llm(pid, pdata)
        if edges:
            stats["success"] += 1
            stats["edges"] += len(edges)
            print(f"{len(edges)} edges")
            for e in edges:
                print(f"    -> {e['to']} [{e['type']}] {e.get('label','')}")
        else:
            stats["failed"] += 1
            print("(no edges)")
        all_llm_edges.extend(edges)

    print(f"\n  Total LLM edges: {stats['edges']} from {stats['success']} pages ({stats['failed']} skipped)")

    if save_to:
        json.dump(all_llm_edges, open(save_to, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"  Saved to {save_to}")

    return all_llm_edges


if __name__ == "__main__":
    if "--llm" in sys.argv:
        run_extraction(DEMO_PAGES)
        llm_edges = run_llm_extraction(DEMO_PAGES, "llm_edges.json")
    else:
        run_extraction(DEMO_PAGES)
        compare_with_handwritten()
        print("\nRun with --llm to invoke LLM extraction.")
