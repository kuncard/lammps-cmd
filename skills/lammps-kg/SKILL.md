---
name: lammps-kg
description: Search 910 LAMMPS commands via 5-layer pipeline — abbrev, spell, stemming, BM25+vector, graph boost. 3214 edges, 911 manual pages.
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

# LAMMPS Knowledge Graph Search

Search 910 LAMMPS command pages with a hybrid retrieval pipeline (BM25 + vector + graph boost).
Returns structured data from the knowledge graph AND full-text excerpts from the scraped manual.
Every result links to docs.lammps.org.

**Self-contained**: `git clone` + `pip install -r requirements.txt` → `python app.py` for web UI,
or `python search_lammps.py search "..."` for CLI.

Script: `search_lammps.py` (in `scripts/`).

## When to use

- Look up LAMMPS command syntax, keyword defaults, or examples
- Search the full manual text for concepts, parameter recommendations, or workflows
- Check command relationships (requires / incompatible / creates / alternative / related)
- Natural language queries like "how to control temperature"
- Autocomplete partial command or keyword names

## Search Pipeline

```
User query
  -> Expand abbreviations + phrases (22 abbrev + 3 phrase maps)
  -> Graph-aware query expansion (QueryExpander: word-to-ID index)
  -> Spell correction (trigram overlap + Levenshtein <= 2)
  -> Stemming (recursive suffix stripping)
  -> BM25 IDF-weighted ranking (k1=1.5, b=0.75)
  -> [+ Vector search: all-mpnet-base-v2 768d, RRF fusion]
  -> Graph boost: neighbor voting via 3214 weighted edges
```

## Commands

### search
```
python search_lammps.py search "nvt thermostat pdamp" --limit 5 [--vector]
```
Returns JSON: ranked results with title, section, score, text preview, URL.

### suggest
```
python search_lammps.py suggest therm
```

### health
```
python search_lammps.py health
```

### detail
```
python search_lammps.py detail fix_nh
```

### neighbors
```
python search_lammps.py neighbors fix_nh
```

## Edge types (weighted)

| Type | Weight | Meaning |
|------|--------|---------|
| requires | 10 | Hard dependency |
| incompatible | 8 | Cannot be used together |
| creates | 7 | Internally creates |
| alternative | 5 | Alternative approach |
| related | 3 | Cross-reference |
| refers_to | 2 | Mentions/references the command |
| howto_ref | 0.8 | How-to guide reference |

## Coverage

910 nodes, 3214 edges. 911 markdown articles across 11 categories:

| Category | Count |
|----------|-------|
| fix | 245 |
| compute | 155 |
| general | 176 |
| pair | 173 |
| howto | 56 |
| angle | 30 |
| bond | 29 |
| dihedral | 20 |
| improper | 17 |
| dump | 8 |
| kspace | 2 |

## Data

- `graph_data_full.json`: 910 nodes, 3214 weighted edges
- `lammps_kb/*.md`: 911 scraped manual pages (full-text search)
- Live links: https://docs.lammps.org/{command}.html
