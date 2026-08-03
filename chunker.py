"""
Markdown chunker — splits LAMMPS documentation articles into searchable chunks.

Produces three chunk types per article:
1. Full-document chunk
2. Section chunks with section_type annotation
3. Sliding-window chunks for long content sections

Shared by bm25_index.py via re-exports.
"""
import re, json, logging
from pathlib import Path

log = logging.getLogger(__name__)


def classify_section(sec_name):
    """Classify a section heading → 'syntax'|'description'|'examples'|'restrictions'|'other'."""
    name_lower = sec_name.lower()
    if any(w in name_lower for w in ("syntax", "parameters", "arguments", "keyword")):
        return "syntax"
    if any(w in name_lower for w in ("description", "overview", "purpose", "theory",
                                      "definition", "introduction")):
        return "description"
    if any(w in name_lower for w in ("example", "usage", "script", "sample")):
        return "examples"
    if any(w in name_lower for w in ("restriction", "note", "warning", "limit",
                                      "caution", "prerequisite", "compatibility")):
        return "restrictions"
    return "other"


def _token_count(text):
    """Rough word count for sliding window."""
    return len(text.split())


def chunk_markdown(md_text, cmd_id, title, phase, url):
    """Split a markdown article into searchable chunks by section.

    Produces three chunk types:
    1. Full-document chunk (entire article)
    2. Section chunks with section_type annotation
    3. Sliding-window chunks for long description sections (preserves cross-section context)
    """
    chunks = []

    # Strip frontmatter
    body = re.sub(r"^---[\s\S]*?---\n*", "", md_text)

    # Extract H1 heading words (e.g. "fix nvt command") for searchability
    h1_match = re.match(r"^# (.+)", body)
    h1_text = h1_match.group(1).strip() if h1_match else ""
    # Title prefix: cmd_id words + title — ensures command name is always searchable
    title_prefix = f"{cmd_id.replace('_', ' ')} {h1_text} {title}. "

    # ── 1. Full-document chunk ──
    full_text = re.sub(r"^#.*\n", "", body).strip()
    if full_text:
        chunks.append({
            "id": f"{cmd_id}__full",
            "cmd_id": cmd_id,
            "section": "full",
            "section_type": "full",
            "title": title,
            "url": url,
            "phase": phase,
            "text": title_prefix + full_text
        })

    # ── 2. Section chunks with type annotation ──
    sections = re.split(r"\n(?=## )", body)
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        # Extract section name from heading
        m = re.match(r"^## (.+)", sec)
        sec_name = m.group(1).strip() if m else "body"
        sec_type = classify_section(sec_name)

        # Clean heading markers for search text
        sec_text = re.sub(r"^#+ .*\n", "", sec, flags=re.MULTILINE).strip()
        # Remove code fences for cleaner text
        sec_text = re.sub(r"```[\s\S]*?```", "", sec_text).strip()
        # Remove markdown formatting
        sec_text = re.sub(r"\*\*(.+?)\*\*", r"\1", sec_text)
        sec_text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", sec_text)
        sec_text = re.sub(r"[-*] ", "", sec_text)

        if len(sec_text) > 20:
            chunks.append({
                "id": f"{cmd_id}__{sec_name.lower().replace(' ','_')[:30]}",
                "cmd_id": cmd_id,
                "section": sec_name,
                "section_type": sec_type,
                "title": title,
                "url": url,
                "phase": phase,
                "text": title_prefix + sec_text
            })

    # ── 3. Sliding-window chunks for long description sections ──
    # Only for key content sections: description, examples
    WINDOW_SIZE = 256   # tokens (rough)
    OVERLAP = 64        # tokens (rough)

    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        m = re.match(r"^## (.+)", sec)
        sec_name = m.group(1).strip() if m else "body"
        sec_type = classify_section(sec_name)

        # Only slide on substantive sections
        if sec_type not in ("description", "examples", "other"):
            continue

        sec_text = re.sub(r"^#+ .*\n", "", sec, flags=re.MULTILINE).strip()
        sec_text = re.sub(r"```[\s\S]*?```", "", sec_text).strip()
        sec_text = re.sub(r"\*\*(.+?)\*\*", r"\1", sec_text)
        sec_text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", sec_text)
        sec_text = re.sub(r"[-*] ", "", sec_text)

        words = sec_text.split()
        if len(words) < WINDOW_SIZE + OVERLAP:
            continue  # section too short to need sliding windows

        # Create overlapping windows
        win_idx = 0
        for start in range(0, len(words) - OVERLAP, WINDOW_SIZE - OVERLAP):
            win_words = words[start:start + WINDOW_SIZE]
            win_text = " ".join(win_words)
            if len(win_text) > 50:
                chunks.append({
                    "id": f"{cmd_id}__{sec_name.lower().replace(' ','_')[:20]}_w{win_idx}",
                    "cmd_id": cmd_id,
                    "section": f"{sec_name} (part {win_idx + 1})",
                    "section_type": sec_type,
                    "title": title,
                    "url": url,
                    "phase": phase,
                    "text": title_prefix + win_text
                })
                win_idx += 1

    return chunks


def build_from_kb(kb_dir):
    """Build chunk list from all markdown files in kb_dir (recursive).

    Args:
        kb_dir: Path to the lammps_kb/ directory.

    Returns:
        List of chunk dicts suitable for BM25Index.build().
    """
    all_chunks = []

    for md_path in sorted(kb_dir.rglob("*.md")):
        if md_path.name == "manifest.json" or "index" in md_path.name.lower():
            continue
        with open(md_path, encoding="utf-8") as f:
            md_text = f.read()

        # Parse frontmatter
        fm = {}
        fm_match = re.match(r"^---\n(.*?)\n---", md_text, re.DOTALL)
        if fm_match:
            for line in fm_match.group(1).strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"')

        cmd_id = fm.get("id", md_path.stem)
        title = fm.get("title", cmd_id)
        phase = fm.get("phase", "")
        url = fm.get("url", "")

        chunks = chunk_markdown(md_text, cmd_id, title, phase, url)
        all_chunks.extend(chunks)

    article_count = len(list(kb_dir.rglob("*.md")))
    log.info("Chunked %s articles into %s chunks", article_count, len(all_chunks))
    return all_chunks
