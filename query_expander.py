"""
Graph-based query expansion — extracts synonym mappings from graph node titles/IDs.

Complements the 22-entry ABBREV dict in abbrev.py by deriving additional
word → command-ID mappings from the knowledge graph structure.
"""
import re
from collections import defaultdict
from abbrev import ABBREV


class QueryExpander:
    """Auto-build synonym expansions from graph node titles and IDs.

    Does NOT expand via graph edges — GraphBooster handles that post-retrieval.
    """

    # Words that are never useful for query expansion
    _STOP_EXPAND = {
        "command", "style", "compute", "fix", "pair", "bond",
        "angle", "dihedral", "improper", "dump", "kspace",
        "atom", "group", "type", "coefficient", "coeff",
        "the", "for", "and", "with", "how", "what",
    }

    # Words already handled by ABBREV (don't duplicate)
    _ABBREV_WORDS = set(ABBREV.keys())

    def __init__(self, nodes, edges=None):
        """Build word→ID index from node IDs and titles.

        Args:
            nodes: list of {id, title, ...} from graph_data_full.json
            edges: ignored (kept for backwards compat with callers that pass edges)
        """
        self.word_to_ids = defaultdict(set)   # "hoover" → {"fix_nh"}
        self.id_to_title = {}                 # "fix_nh" → "fix nvt command"
        self.id_to_words = defaultdict(set)   # "fix_nh" → {"nvt","nose","hoover"}
        self._build(nodes)

    def _split_words(self, text):
        """Extract meaningful words from a title/ID string."""
        parts = re.split(r'[ _\-/]+', text.lower())
        return {p.strip() for p in parts if len(p.strip()) >= 2}

    def _build(self, nodes):
        """Build word→ID index from node IDs (exact split) and titles."""
        for n in nodes:
            nid = n["id"]
            title = n.get("title", nid)
            self.id_to_title[nid] = title

            id_words = self._split_words(nid)
            title_words = self._split_words(title)

            for w in id_words | title_words:
                if w not in self._STOP_EXPAND and w not in self._ABBREV_WORDS:
                    self.word_to_ids[w].add(nid)
                    self.id_to_words[nid].add(w)

        # Remove words that match too many nodes (low specificity)
        for w in list(self.word_to_ids.keys()):
            if len(self.word_to_ids[w]) > 8:
                del self.word_to_ids[w]

    def expand(self, query, max_expansions=6):
        """Expand query with specific synonyms from the graph.

        Only expands tokens that map to 1-5 nodes (highly specific).
        Tokens already in ABBREV dict are skipped (ABBREV is more authoritative).
        """
        qt = query.lower()
        tokens = re.findall(r"[a-z0-9]{2,}", qt)
        if not tokens:
            return query

        expansions = []
        seen_ids = set()

        for token in tokens:
            if token in self._ABBREV_WORDS:
                continue

            matched_ids = self.word_to_ids.get(token, set())
            if len(matched_ids) > 5:
                continue

            for mid in sorted(matched_ids):  # sorted for determinism
                if mid in seen_ids:
                    continue
                seen_ids.add(mid)
                title = self.id_to_title.get(mid, mid)
                title_words = [w for w in self._split_words(title)
                               if w not in self._STOP_EXPAND and w not in self._ABBREV_WORDS]
                expansions.append(" ".join(title_words))

            if len(expansions) >= max_expansions:
                break

        if not expansions:
            return query

        exp_text = " ".join(expansions[:max_expansions])
        return f"{query} {exp_text}"
