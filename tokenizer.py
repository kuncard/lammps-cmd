"""
Tokenizer for LAMMPS documentation search.
Extracts compound terms (with _, /, -) and plain tokens, with stop-word removal.

Shared by bm25_index.py and search_lammps.py via bm25_index re-exports.
"""
import re

STOP_WORDS = {
    "the","a","an","is","are","was","were","be","been","being","have","has","had",
    "do","does","did","will","would","shall","should","may","might","must","can",
    "could","i","me","my","we","our","you","your","he","she","it","they","them",
    "this","that","these","those","and","or","but","not","no","if","then","else",
    "when","where","why","how","all","each","every","both","few","more","most",
    "some","such","only","own","same","so","than","too","very","in","on","at",
    "to","for","of","from","by","with","about","into","through","during","before",
    "after","above","below","between","up","down","out","off","over","under",
    "again","further","once","here","there","now","also","just","well","get"
}


def tokenize(text):
    """Lowercase, extract tokens >= 2 chars. Preserves _, /, - for compound terms.

    Strategy: emit both compound tokens AND their split parts.
    "fix_nh"      → ["fix_nh", "fix", "nh"]
    "Nose-Hoover" → ["nose-hoover", "nose", "hoover"]
    "lj/cut"      → ["lj/cut", "lj", "cut"]
    This keeps high-IDF LAMMPS command names while still matching individual words.
    """
    tokens = []
    # Match compound tokens (with _, /, or -)
    compounds = re.findall(r"[a-z0-9]+(?:[/_-][a-z0-9]+)+", text.lower())
    tokens.extend(compounds)
    # Also split compounds into individual parts
    for c in compounds:
        tokens.extend(re.split(r"[/_-]", c))
    # Match plain tokens (no _, /, or -)
    plain = re.findall(r"(?<![a-z0-9/_-])[a-z0-9]{2,}(?![a-z0-9/_-])", text.lower())
    tokens.extend(plain)
    return [t for t in tokens if len(t) >= 2 and t not in STOP_WORDS]
