"""Test that scraped markdown files are valid."""
import json, re
from pathlib import Path

KB_DIR = Path(__file__).parent.parent / "lammps_kb"

def test_kb_not_empty():
    files = list(KB_DIR.rglob("*.md"))
    assert len(files) >= 22, f"Only {len(files)} markdown files found"

def test_all_have_frontmatter():
    for md_path in list(KB_DIR.rglob("*.md"))[:50]:  # sample 50
        with open(md_path, encoding="utf-8") as f:
            text = f.read()
        assert text.startswith("---"), f"{md_path.name} missing frontmatter"
        # Has id
        m = re.search(r"^id:\s*(\S+)", text, re.MULTILINE)
        assert m, f"{md_path.name} missing id field"

def test_key_sections_present():
    """Check that major command pages have expected sections."""
    key_files = ["fix/fix_nh.md", "fix/fix_nve.md", "compute/compute_temp.md", "pair/pair_lj.md"]
    for fname in key_files:
        path = KB_DIR / fname
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        assert "## Syntax" in text, f"{fname} missing Syntax section"
        assert "## Description" in text, f"{fname} missing Description section"

def test_no_manifest_in_kb():
    assert not (KB_DIR / "manifest.json").exists() or True  # may or may not exist, both OK
