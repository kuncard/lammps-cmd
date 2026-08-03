"""Test 5-layer search pipeline."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "lammps-kg" / "scripts"))
from search_lammps import search, suggest, health, detail, neighbors, _init

def test_health():
    h = health()
    assert h["status"] == "ok"
    assert h["nodes"] >= 22
    assert h["edges"] >= 47

def test_exact_command():
    r = search("fix nvt", limit=5)
    assert r["total"] >= 1
    ids = [x["cmd_id"] for x in r["results"]]
    # fix_nvt variants all come from fix_nh family
    assert any(i.startswith("fix_nvt") or i == "fix_nh" for i in ids)

def test_spell_correction():
    r = search("boundry condition", limit=5)
    ids = [x["cmd_id"] for x in r["results"]]
    assert "boundary" in ids

def test_abbreviation():
    r = search("nvt pdamp default", limit=5)
    ids = [x["cmd_id"] for x in r["results"]]
    assert "fix_nh" in ids

def test_natural_language():
    r = search("how to initialize velocities at 300K", limit=5)
    ids = [x["cmd_id"] for x in r["results"]]
    assert "velocity" in ids

def test_suggest():
    s = suggest("ther")
    suggestions = s["suggestions"]
    assert len(suggestions) >= 2
    assert any("thermo" in x.lower() for x in suggestions)

def test_detail():
    d = detail("fix_nh")
    assert "title" in d
    assert "keywords" in d

def test_neighbors():
    n = neighbors("fix_nh")
    assert "relationships" in n
    assert len(n["relationships"]) >= 1

def test_no_self_loops():
    from search_lammps import _EDGES
    for e in _EDGES:
        assert e["from"] != e["to"], f"Self-loop: {e['from']} -> {e['to']}"
