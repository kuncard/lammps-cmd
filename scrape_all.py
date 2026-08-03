"""
Scrape LAMMPS command documentation pages from docs.lammps.org.
Generates categorized markdown knowledge base.

Usage:
  python scrape_all.py                    # full scrape (911 pages)
  python scrape_all.py --diff             # incremental: only new/changed pages
  python scrape_all.py --categories fix   # scrape specific category
  python scrape_all.py --limit 10         # limit for testing
"""
import requests, json, re, os, sys, time, argparse, hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

from logging_setup import setup_logging
log = setup_logging(__name__)

ROOT = Path(__file__).parent
KB_DIR = ROOT / "lammps_kb"
SITEMAP_URL = "https://docs.lammps.org/sitemap.xml"

# Scientific symbols → ASCII equivalents (preserve meaning, not just strip)
_SCI_MAP = {
    "Å": "Angstrom",   # Å
    "Å": "Angstrom",   # Å
    "°": "deg",        # °
    "±": "+/-",        # ±
    "×": "x",          # ×
    "µ": "u",          # µ (micro)
    "α": "alpha",      # α
    "β": "beta",       # β
    "γ": "gamma",      # γ
    "δ": "delta",      # δ
    "ε": "epsilon",    # ε
    "θ": "theta",      # θ
    "λ": "lambda",     # λ
    "σ": "sigma",      # σ
    "φ": "phi",        # φ
    "ω": "omega",      # ω
    "²": "^2",         # ²
    "³": "^3",         # ³
    "–": "--",         # – (en-dash)
    "—": "--",         # — (em-dash)
    "‘": "'",          # ‘
    "’": "'",          # ’
    "“": '"',          # "
    "”": '"',          # "
}
_SCI_RE = re.compile("|".join(re.escape(k) for k in _SCI_MAP))


def clean_text(text):
    """Clean scraped text: map scientific symbols → ASCII, strip remaining non-ASCII."""
    text = text.replace("\xa0", " ").replace("\xb6", "")
    # Map known scientific symbols to ASCII equivalents
    text = _SCI_RE.sub(lambda m: _SCI_MAP[m.group(0)], text)
    # Strip any remaining non-ASCII (rare CJK / emoji that slipped through)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def fetch_page(url, timeout=30):
    headers = {"User-Agent": "LAMMPS-KB/1.0"}
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            if attempt == 2: raise
            time.sleep(2)

def get_command_urls(categories=None):
    """Extract command page URLs from sitemap.xml."""
    log.info("Fetching sitemap...")
    # Use cached copy if available
    cache_path = KB_DIR / "sitemap.xml"
    if cache_path.exists():
        log.info("  Using cached sitemap.xml")
        text = cache_path.read_text(encoding="utf-8")
    else:
        resp = requests.get(SITEMAP_URL, timeout=30)
        text = resp.text
        # Cache for future runs
        KB_DIR.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(text, encoding="utf-8")
    all_urls = set(re.findall(r'<loc>(https://docs\.lammps\.org/[^<]+)</loc>', text))

    # Categorize URLs
    patterns = {
        "fix": re.compile(r'/fix_\w+\.html'),
        "compute": re.compile(r'/compute_\w+\.html'),
        "pair": re.compile(r'/pair_\w+\.html'),
        "bond": re.compile(r'/bond_\w+\.html'),
        "angle": re.compile(r'/angle_\w+\.html'),
        "dihedral": re.compile(r'/dihedral_\w+\.html'),
        "improper": re.compile(r'/improper_\w+\.html'),
        "dump": re.compile(r'/dump_\w+\.html'),
        "kspace": re.compile(r'/kspace_\w+\.html'),
        "howto": re.compile(r'/Howto_\w+\.html'),
        "general": re.compile(r'/(?!fix_|compute_|pair_|bond_|angle_|dihedral_|improper_|dump_|kspace_|Howto_|Commands_|Build_|Developer_|Errors_|Classes_|Library_|Python_|Speed_|Manual|Modify|Run_)([a-z_]+)\.html'),
    }

    cats = categories or list(patterns.keys())
    selected = {}
    for cat in cats:
        if cat in patterns:
            matched = sorted(u for u in all_urls if patterns[cat].search(u))
            selected[cat] = matched

    total = sum(len(v) for v in selected.values())
    for cat, urls_list in selected.items():
        log.info("  %s: %s pages", cat, len(urls_list))
    log.info("  Total: %s pages", total)
    return selected

def extract_markdown(html, page_id, url):
    """Parse Sphinx HTML into markdown."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["nav","footer","script","style","head","link","meta"]):
        tag.decompose()

    h1 = soup.find("h1")
    title = clean_text(h1.get_text()) if h1 else page_id

    sections = soup.find_all("section")
    if not sections:
        # Not a command page — still try to get content
        body = soup.find("body") or soup
        text = clean_text(body.get_text())
        return {"title": title, "content": text[:5000], "is_command": False}

    # Extract sections
    syntax, examples, description, restrictions, related = "", "", "", "", ""
    for sec in sections:
        sec_id = sec.get("id","").lower()
        txt = clean_text(sec.get_text())

        if sec_id == "syntax":
            pres = sec.find_all("pre")
            syntax = "\n".join(clean_text(p.get_text()) for p in pres) if pres else txt
        elif sec_id == "examples":
            pres = sec.find_all("pre")
            examples = "\n\n".join(f"```\n{clean_text(p.get_text())}\n```" for p in pres) if pres else txt
        elif sec_id == "description":
            parts = []
            for child in sec.children:
                if child.name == "pre":
                    t = clean_text(child.get_text())
                    if t: parts.append(f"```\n{t}\n```")
                elif child.name in ("p","div"):
                    t = clean_text(child.get_text())
                    if t: parts.append(t)
            description = "\n\n".join(parts) if parts else txt
        elif sec_id == "restrictions":
            restrictions = txt
        elif "related" in sec_id:
            links = []
            for a in sec.find_all("a", href=True):
                lt = clean_text(a.get_text())
                if lt and "http" not in a["href"]:
                    links.append(f"- [{lt}]({a['href']})")
            related = "\n".join(links) if links else txt

    # Keywords from definition lists
    dls = soup.find_all("dl")
    kw_parts = []
    for dl in dls:
        for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd")):
            kn = clean_text(dt.get_text())
            kd = clean_text(dd.get_text())
            if kn and "{" not in kn:
                kw_parts.append(f"- **{kn}**: {kd}")
    keywords = "\n".join(kw_parts)

    # Assemble markdown
    md = f"""---
id: {page_id}
title: "{title}"
url: {url}
---

# {title}

"""
    if syntax: md += f"## Syntax\n\n```\n{syntax}\n```\n\n"
    if description: md += f"## Description\n\n{description}\n\n"
    if keywords: md += f"## Keywords\n\n{keywords}\n\n"
    if examples: md += f"## Examples\n\n{examples}\n\n"
    if restrictions: md += f"## Restrictions\n\n{restrictions}\n\n"
    if related: md += f"## Related Commands\n\n{related}\n\n"

    return {"title": title, "content": md, "is_command": True,
            "related_links": re.findall(r'\[(.*?)\]\((.*?)\)', related) if related else []}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--categories", default="fix,compute,pair,bond,angle,dihedral,improper,dump,kspace,howto,general")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--diff", action="store_true",
                    help="Incremental mode: re-scrape all, but only overwrite changed pages")
    args = ap.parse_args()

    cats = [c.strip() for c in args.categories.split(",")]
    selected = get_command_urls(cats)

    # Flatten
    all_pages = []
    for cat, urls in selected.items():
        for url in urls:
            page_id = url.split("/")[-1].replace(".html","").replace("#","__")
            all_pages.append((cat, page_id, url))

    # In --diff mode: re-scrape all, only update changed. Otherwise: skip existing.
    if args.diff:
        pending = all_pages  # Re-scrape everything
        log.info("  Diff mode: will check %s pages for changes", len(pending))
    else:
        pending = []
        for cat, pid, url in all_pages:
            out_path = KB_DIR / cat / f"{pid}.md"
            if out_path.exists():
                continue
            pending.append((cat, pid, url))
        log.info("  Already done: %s, Pending: %s", len(all_pages) - len(pending), len(pending))

    if args.limit:
        pending = pending[args.start:args.start+args.limit]
        log.info("  Limited to %s pages", len(pending))

    # Create category directories
    for cat in cats:
        (KB_DIR / cat).mkdir(parents=True, exist_ok=True)

    # Scrape
    manifest = {"total": len(all_pages), "pages": []}
    counts = defaultdict(lambda: {"ok":0, "fail":0, "skipped":0, "unchanged":0})
    start_time = time.time()

    for i, (cat, page_id, url) in enumerate(pending):
        out_path = KB_DIR / cat / f"{page_id}.md"
        if i % 20 == 0 and i > 0:
            elapsed = time.time() - start_time
            rate = i / elapsed
            remaining = (len(pending) - i) / rate
            log.info("  ... %s/%s (%.1f pg/s, ETA %.0fs)", i, len(pending), rate, remaining)

        try:
            html = fetch_page(url)
            time.sleep(0.15)  # Be polite
            result = extract_markdown(html, page_id, url)

            if not result.get("is_command"):
                counts[cat]["skipped"] += 1
                continue

            new_content = result["content"]
            new_hash = hashlib.md5(new_content.encode()).hexdigest()

            # In --diff mode: skip if unchanged
            if args.diff and out_path.exists():
                old_hash = hashlib.md5(out_path.read_text(encoding="utf-8").encode()).hexdigest()
                if old_hash == new_hash:
                    counts[cat]["unchanged"] += 1
                    continue  # No change, skip

            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            tag = "UPDATED" if out_path.exists() and args.diff else "NEW"
            manifest["pages"].append({
                "id": page_id, "category": cat, "url": url,
                "title": result["title"], "file": str(out_path.relative_to(KB_DIR))
            })
            counts[cat]["ok"] += 1

        except Exception as e:
            counts[cat]["fail"] += 1
            if counts[cat]["fail"] <= 3:
                log.error("  FAIL [%s]: %s", page_id, e)

    # Save manifest
    manifest["categories"] = {cat: {"ok": c["ok"], "fail": c["fail"], "skipped": c["skipped"]}
                              for cat, c in counts.items()}
    manifest["built_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(KB_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Summary
    total_ok = sum(c["ok"] for c in counts.values())
    total_fail = sum(c["fail"] for c in counts.values())
    log.info("Done: %s OK, %s fail, %s total in %.0fs", total_ok, total_fail, total_ok + total_fail, time.time() - start_time)
    log.info("Output: %s/", KB_DIR)
    return total_fail == 0

if __name__ == "__main__":
    main()
