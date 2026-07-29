---
name: lammps-kg
description: Search LAMMPS manual — NVT/NPT MD commands with syntax, keywords, defaults, and weighted relationship graph. 22 commands, 47 edges, live doc links.
metadata:
  tools:
    - run_skill_script
  dependent_skills: []
  tags:
    - lammps
    - md
    - knowledge
    - search
---

# LAMMPS Command Search — NVT/NPT

Search 22 LAMMPS command pages for NVT/NPT molecular dynamics. Each result includes
syntax, keywords table (type/default/description), examples, and live doc links.

**Relationship-aware**: results include graph neighbors with labeled edge types
(requires / creates / incompatible / alternative / see also).

Script: `search_lammps.py` (in `scripts/`).

## When to use

- Look up a LAMMPS command syntax, keyword defaults, or examples
- Find which commands are needed before using fix nvt/npt
- Understand command relationships (what requires what, what creates what)
- Check parameter defaults before writing input scripts
- Explore NVT/NPT workflow: init → build → force → integrator → output

## Commands

### search — Search LAMMPS commands

```
run_skill_script(
    skill_name="lammps-kg",
    script_name="search_lammps.py",
    args="search 'fix nvt' --limit 5"
)
```

Returns JSON: ranked results with title, synopsis, syntax, keywords, examples, URL.

Options: `--limit N`, `--phase TYPE`, `--verbose`

### detail — Get full command documentation

```
run_skill_script(
    skill_name="lammps-kg",
    script_name="search_lammps.py",
    args="detail fix_nh"
)
```

Returns full structured data: syntax, keywords table, examples, restrictions, relationships.

### neighbors — Get related commands

```
run_skill_script(
    skill_name="lammps-kg",
    script_name="search_lammps.py",
    args="neighbors fix_nh"
)
```

Returns all connected commands grouped by relationship type.

## Edge types (weighted)

| Type | Weight | Meaning |
|------|--------|---------|
| requires | 10 | Hard dependency — "must set before" |
| incompatible | 8 | "do NOT use with" |
| creates | 7 | "internally creates" |
| howto_ref | 3 | Tutorial discusses this command |
| related | 2 | Cross-reference / see also |

## Data

22 commands covering the NVT/NPT MD workflow:
Initialize → Build System → Force Field → Integrator → Compute → Output → Guides

Live doc links: https://docs.lammps.org/{command}.html
