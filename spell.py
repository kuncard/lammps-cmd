"""
Trigram-based spell corrector for LAMMPS search queries.
Built from document vocabulary to correct typos in technical terms.

Shared by bm25_index.py via re-exports.
"""
from tokenizer import tokenize


class SpellCorrector:
    """Trigram-based spell correction. Built from chunk vocabulary."""

    def __init__(self):
        self.trigrams = {}
        self.vocab = set()

    def build(self, words):
        """Index words by character trigrams."""
        for w in words:
            w = w.lower()
            self.vocab.add(w)
            padded = "  " + w + " "
            for i in range(len(padded) - 2):
                tg = padded[i:i + 3]
                if tg not in self.trigrams:
                    self.trigrams[tg] = set()
                self.trigrams[tg].add(w)

    def correct(self, word):
        """Return (corrected_word, confidence)."""
        w = word.lower()
        if w in self.vocab or len(w) <= 2:
            return w, 1.0 if w in self.vocab else 0.0

        padded = "  " + w + " "
        tw = {padded[i:i + 3] for i in range(len(padded) - 2)}

        candidates = {}
        for tg in tw:
            for c in self.trigrams.get(tg, set()):
                candidates[c] = candidates.get(c, 0) + 1

        if not candidates:
            return w, 0.0

        best, best_score = w, 0
        for c, overlap in candidates.items():
            if len(c) <= 2:
                continue
            dist = self._edit_dist(w, c)
            if dist <= 2:
                score = overlap / max(len(w), len(c))
                if score > best_score:
                    best_score, best = score, c
        return best, best_score if best != w else 0.0

    @staticmethod
    def _edit_dist(a, b):
        """Levenshtein distance."""
        if len(a) < len(b):
            a, b = b, a
        prev = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            cur = [i]
            for j, cb in enumerate(b, 1):
                cur.append(min(prev[j] + 1, cur[-1] + 1,
                               prev[j - 1] + (0 if ca == cb else 1)))
            prev = cur
        return prev[-1]


def correct_query(query, spell):
    """Apply spell correction to each token in the query.

    Only corrects tokens NOT already in vocab (avoids corrupting technical terms).
    Requires confidence > 0.7 to avoid false corrections.

    Args:
        query: raw query string
        spell: SpellCorrector instance (from BM25Index.spell)
    """
    tokens = tokenize(query)
    corrected = []
    for t in tokens:
        if t in spell.vocab:
            corrected.append(t)  # already known — don't touch
        else:
            c, conf = spell.correct(t)
            corrected.append(c if conf > 0.7 else t)
    return " ".join(corrected)
