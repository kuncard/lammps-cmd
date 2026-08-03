"""
BM25 search index for markdown knowledge base chunks.
Generalized from cmd_search.py MiniBM25 to work with {id, text} dicts.

Usage:
  python bm25_index.py --build              # build index from lammps_kb/*.md
  python bm25_index.py --search "Tdamp"     # test search
"""
import json, re, math, argparse, logging
from pathlib import Path

log = logging.getLogger(__name__)

ROOT = Path(__file__).parent
KB_DIR = ROOT / "lammps_kb"
INDEX_FILE = KB_DIR / "bm25_index.json"

# ── Tokenizer (extracted to tokenizer.py, re-exported for backwards compat) ──
from tokenizer import STOP_WORDS, tokenize  # noqa: F401 — re-export


# ── ABBREV Expansion (shared single source of truth) ──
from abbrev import ABBREV as _ABBREV_MAP, PHRASE_MAP
# Sort by length descending: lj/cut must match before lj inside "lj/cut"
_ABBREV_KEYS = sorted(_ABBREV_MAP, key=len, reverse=True)
_ABBREV_RE = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in _ABBREV_KEYS) + r')\b',
    re.IGNORECASE
)

def expand_query(query):
    """Expand abbreviations and essential phrases in query text."""
    # 1. Phrase-level expansion
    ql = query.lower()
    for phrase, expansion in PHRASE_MAP:
        if phrase in ql:
            query = query + " " + expansion

    # 2. Single-word abbreviation expansion
    def _replace(m):
        w = m.group(0).lower()
        return m.group(0) + " " + _ABBREV_MAP.get(w, "")
    return _ABBREV_RE.sub(_replace, query)


# ── Spell Corrector (extracted to spell.py, re-exported for backwards compat) ──
from spell import SpellCorrector, correct_query  # noqa: F401 — re-export


# ── Unified Query Classification ──
# Shared by Flask (app.py) and CLI (search_lammps.py).
# Both paths call classify_query() for consistent behavior.

_PARAM_WORDS = {"default", "value", "unit", "recommend", "setting",
                "parameter", "option", "flag", "syntax", "format",
                "tdamp", "pdamp", "timestep", "cutoff"}

_QUESTION_WORDS = {"how", "what", "why", "which", "when", "where",
                   "can", "does", "explain", "describe"}


def classify_query(query, known_commands=None):
    """Classify a LAMMPS search query → ('command'|'natural'|'param', strategy).

    known_commands: optional set of known command IDs / tokens from the graph
                    (when available, enables precise command-name detection).

    Strategy dict keys:
      - bm25_weight, vec_weight : RRF fusion weights (Flask path)
      - bm25_limit              : search limit before RRF / graph boost
      - section_boost           : 'structured' or None (CLI path)
    """
    # Full tokens (preserves _ compounds like fix_nh, angle_coeff)
    q_words = set(tokenize(query))
    # Raw word tokens (includes stop words — needed for question-word detection)
    raw_words = set(re.findall(r"[a-z0-9]{2,}", query.lower()))

    # 0. Underscore compound → almost certainly a LAMMPS command name
    has_underscore_cmd = any("_" in w for w in q_words)

    # 1. Exact command name in query (requires graph-loaded cmdset)
    if known_commands and (q_words & known_commands):
        return "command", {
            "bm25_weight": 1.0, "vec_weight": 0.3,
            "bm25_limit": 10, "section_boost": None,
        }

    # 2. Underscore compound (e.g. fix_nh, angle_coeff) → command query
    #    even if question words are also present
    if has_underscore_cmd:
        return "command", {
            "bm25_weight": 1.0, "vec_weight": 0.3,
            "bm25_limit": 10, "section_boost": None,
        }

    # 3. Parameter / syntax lookup (check raw_words: pdamp, timestep might be in vocab)
    if raw_words & _PARAM_WORDS:
        return "param", {
            "bm25_weight": 1.0, "vec_weight": 0.5,
            "bm25_limit": 20, "section_boost": "structured",
        }

    # 4. Natural-language / conceptual (use raw_words: "how","what" are stop words)
    if raw_words & _QUESTION_WORDS:
        return "natural", {
            "bm25_weight": 0.9, "vec_weight": 0.6,
            "bm25_limit": 20, "section_boost": None,
        }

    # 5. Default: treat as command-style keyword search
    return "command", {
        "bm25_weight": 1.0, "vec_weight": 0.3,
        "bm25_limit": 10, "section_boost": None,
    }


# ── BM25 Index ──
class BM25Index:
    """BM25 search index. k1=1.5, b=0.75 (standard)."""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = []        # list of {id, text, metadata}
        self.N = 0
        self.doc_len = []     # token count per doc
        self.avgdl = 0
        self.df = {}          # term → document frequency
        self.tf = []          # per doc: term → term frequency
        self.spell = SpellCorrector()  # per-instance spell corrector
        self._built = False

    def build(self, docs):
        """Build index from list of {id, text, metadata} dicts."""
        self.docs = list(docs)
        self.N = len(self.docs)

        if self.N == 0:
            self._built = True
            return

        self.doc_len = []
        self.tf = []
        self.df = {}

        for d in self.docs:
            tokens = tokenize(d["text"])
            self.doc_len.append(len(tokens))

            # Term frequencies for this doc
            doc_tf = {}
            for t in tokens:
                doc_tf[t] = doc_tf.get(t, 0) + 1
            self.tf.append(doc_tf)

            # Document frequencies
            for t in set(tokens):
                self.df[t] = self.df.get(t, 0) + 1

        self.avgdl = sum(self.doc_len) / self.N if self.N > 0 else 0
        self._built = True

        # Build spell corrector vocabulary from indexed tokens + ABBREV terms
        self.spell = SpellCorrector()
        self.spell.build(list(self.df.keys()))
        extra_words = set()
        for v in _ABBREV_MAP.values():
            extra_words.update(tokenize(v))
        self.spell.build(list(extra_words))

    def search(self, query, limit=10, query_type="command", expand=True):
        """BM25 search. Returns [{id, text, metadata, score}, ...]."""
        if not self._built or self.N == 0:
            return []

        # Lazy-build spell corrector if not yet initialized (e.g. loaded from disk)
        if len(self.spell.vocab) == 0 and len(self.df) > 0:
            self.spell.build(list(self.df.keys()))

        # Expand abbreviations (skip if caller already did)
        if expand:
            query = expand_query(query)
        query = correct_query(query, self.spell)
        q_tokens = tokenize(query)
        if not q_tokens:
            return []

        # IDF for query terms
        idf = {}
        for t in q_tokens:
            n = self.df.get(t, 0)
            idf[t] = math.log((self.N - n + 0.5) / (n + 0.5) + 1.0)

        # Score each doc
        scores = []
        for i, doc_tf in enumerate(self.tf):
            dl = self.doc_len[i]
            if dl == 0:
                continue
            score = 0.0
            for t in q_tokens:
                if t not in doc_tf:
                    continue
                tf_td = doc_tf[t]
                numerator = tf_td * (self.k1 + 1)
                denominator = tf_td + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                score += idf.get(t, 0) * numerator / denominator

            # Title + cmd_id boost: check query tokens in title and cmd_id combined
            title_lower = self.docs[i].get("title", "").lower()
            cmd_id_lower = self.docs[i].get("cmd_id", "").lower()
            boost_text = title_lower + " " + cmd_id_lower
            boost_hits = sum(1 for t in q_tokens if t in boost_text)
            if boost_hits > 0:
                score *= 1.0 + 0.3 * boost_hits

            # Canonical boost: prefer shorter cmd_ids (generic > variant)
            # fix_nh (2 segments) > fix_nvt_sphere (3 segments)
            cmd_parts = cmd_id_lower.split("_")
            if len(cmd_parts) <= 2 and score > 0:
                score *= 1.20

            # Section-type boost: param queries → syntax, natural queries → description
            if query_type == "param" and self.docs[i].get("section_type") == "syntax":
                score *= 1.15
            if query_type == "natural" and self.docs[i].get("section_type") == "description":
                score *= 1.10

            # Long-doc penalty: penalize docs with many chunks (>8 = very long)
            cmd = self.docs[i].get("cmd_id", "")
            if cmd:
                chunk_count = sum(1 for d in self.docs if d.get("cmd_id") == cmd)
                if chunk_count > 8:
                    score *= 0.92

            if score > 0:
                scores.append({**self.docs[i], "score": round(score, 4)})

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:limit]

    def save(self, path=None):
        """Serialize index to JSON."""
        p = Path(path or INDEX_FILE)
        data = {
            "k1": self.k1, "b": self.b,
            "N": self.N, "avgdl": self.avgdl,
            "docs": self.docs,
            "doc_len": self.doc_len,
            "df": self.df,
            "tf": [dict(tf) for tf in self.tf]
        }
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        log.info("BM25 index saved: %s (%s docs)", p, self.N)

    def load(self, path=None):
        """Load index from JSON."""
        p = Path(path or INDEX_FILE)
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        self.k1 = data["k1"]; self.b = data["b"]
        self.N = data["N"]; self.avgdl = data["avgdl"]
        self.docs = data["docs"]
        self.doc_len = data["doc_len"]
        self.df = data["df"]
        self.tf = data["tf"]
        self._built = True
        log.info("BM25 index loaded: %s (%s docs)", p, self.N)


# ── Chunk maker (extracted to chunker.py, re-exported for backwards compat) ──
from chunker import classify_section, chunk_markdown, build_from_kb as _build_from_kb  # noqa: F401


def build_from_kb():
    """Build BM25 index from all markdown files in lammps_kb/ (recursive).

    Thin wrapper around chunker.build_from_kb() that passes the project's KB_DIR.
    """
    return _build_from_kb(KB_DIR)


# ── CLI ──
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--search", type=str)
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    if args.build:
        chunks = build_from_kb()
        idx = BM25Index()
        idx.build(chunks)
        idx.save()
        print(f"  Chunks: {idx.N}, avg len: {idx.avgdl:.1f} tokens")

    if args.search:
        idx = BM25Index()
        idx.load()
        results = idx.search(args.search, args.limit)
        for i, r in enumerate(results):
            print(f"  [{i+1}] {r['cmd_id']}/{r['section']} (score={r['score']})")
            print(f"       {r['text'][:120]}...")
            print()
