"""
Vector search index using local sentence-transformers embeddings (all-mpnet-base-v2, 768d).

Usage:
  python vector_index.py --build              # build embeddings
  python vector_index.py --search "Tdamp"     # test search
"""
import json, argparse, logging, numpy as np
from pathlib import Path

log = logging.getLogger(__name__)

ROOT = Path(__file__).parent
KB_DIR = ROOT / "lammps_kb"
EMB_FILE = KB_DIR / "embeddings.npy"
CHUNKS_FILE = KB_DIR / "chunks_for_index.json"

# ── Lazy-loaded local embedding model ──
_LOCAL_MODEL = None
_LOCAL_MODEL_NAME = "all-mpnet-base-v2"  # 768d, ~420MB, stronger semantic matching


def _get_local_model():
    """Lazy-load sentence-transformers model (singleton).

    Returns model on success, None if model can't be loaded (no internet, etc).
    Caller should fall back to BM25-only mode.
    """
    global _LOCAL_MODEL
    if _LOCAL_MODEL is not None:
        return _LOCAL_MODEL
    if _LOCAL_MODEL is False:  # previously failed
        return None

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        log.warning("sentence-transformers not installed. Run: pip install sentence-transformers")
        log.warning("Falling back to BM25-only mode (no vector search).")
        _LOCAL_MODEL = False
        return None

    log.info("Loading embedding model: %s ...", _LOCAL_MODEL_NAME)
    log.info("(First run downloads ~420MB. If slow, Ctrl+C and use --skip-vector)")
    try:
        _LOCAL_MODEL = SentenceTransformer(_LOCAL_MODEL_NAME)
    except Exception as e:
        log.error("Model load failed: %s", e)
        log.error("Check internet connection or download model manually")
        _LOCAL_MODEL = False
        return None

    dim = _LOCAL_MODEL.get_embedding_dimension() if hasattr(_LOCAL_MODEL, 'get_embedding_dimension') else _LOCAL_MODEL.get_sentence_embedding_dimension()
    log.info("Model loaded. dim=%s", dim)
    return _LOCAL_MODEL


class VectorIndex:
    """Semantic search using local sentence-transformers (all-mpnet-base-v2, 768d)."""

    def __init__(self):
        self.chunks = []
        self.embeddings = None  # numpy array (N, D), L2-normalized
        self.dim = 0

    def _embed(self, texts):
        """Encode texts with local sentence-transformers model."""
        model = _get_local_model()
        arr = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=(len(texts) > 100),
            batch_size=32,
        )
        return arr

    def build(self, chunks):
        """Encode all chunks into normalized embedding vectors."""
        self.chunks = list(chunks)

        if len(self.chunks) == 0:
            self.embeddings = np.zeros((0, 1), dtype=np.float32)
            self.dim = 0
            log.warning("No chunks to embed.")
            return

        # Truncate long texts for embedding efficiency
        texts = [c["text"][:2000] for c in self.chunks]
        log.info("Encoding %s chunks via local sentence-transformers ...", len(texts))

        self.embeddings = self._embed(texts)
        self.dim = self.embeddings.shape[1]
        log.info("Done: %s chunks, %sd", self.embeddings.shape[0], self.dim)

    def search(self, query, top_k=10):
        """Cosine similarity search. Returns [{...chunk, score}, ...]."""
        if self.embeddings is None or len(self.chunks) == 0:
            return []
        if self.embeddings.shape[0] == 0:
            return []

        # Embed query
        q_arr = self._embed([query[:2000]])
        q_vec = q_arr[0]

        # Cosine similarity (embeddings are already L2-normalized)
        scores = np.dot(self.embeddings, q_vec)
        top_idx = np.argsort(scores)[::-1][:top_k]

        return [
            {**self.chunks[i], "score": round(float(scores[i]), 4)}
            for i in top_idx if scores[i] > 0.1
        ]

    def save(self):
        """Save embeddings and chunks to disk."""
        if self.embeddings is None:
            log.warning("Nothing to save (embeddings is None).")
            return
        KB_DIR.mkdir(parents=True, exist_ok=True)
        np.save(EMB_FILE, self.embeddings)
        meta = {
            "chunks": self.chunks,
            "dim": int(self.embeddings.shape[1]),
            "model_name": _LOCAL_MODEL_NAME,
        }
        with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False)
        log.info("Vector index saved: %s (%s chunks, %sd, %s)", EMB_FILE, len(self.chunks), self.dim, _LOCAL_MODEL_NAME)

    def load(self):
        """Load embeddings and chunks from disk. Returns True on success."""
        if not EMB_FILE.exists() or not CHUNKS_FILE.exists():
            log.warning("Index files not found. Run --build first.")
            return False

        self.embeddings = np.load(EMB_FILE)
        with open(CHUNKS_FILE, encoding="utf-8") as f:
            meta = json.load(f)
        if isinstance(meta, list):
            # Legacy format: bare list of chunks
            self.chunks = meta
            self.dim = self.embeddings.shape[1]
        else:
            self.chunks = meta["chunks"]
            self.dim = meta.get("dim", self.embeddings.shape[1])
        log.info("Vector index loaded: %s chunks, %sd, %s", len(self.chunks), self.dim, _LOCAL_MODEL_NAME)
        return True


# ── CLI ──
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--search", type=str)
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()

    if args.build:
        import sys
        sys.path.insert(0, str(ROOT))
        from bm25_index import build_from_kb
        chunks = build_from_kb()
        vi = VectorIndex()
        vi.build(chunks)
        vi.save()

    if args.search:
        vi = VectorIndex()
        if not vi.load():
            import sys; sys.exit(1)
        results = vi.search(args.search, args.limit)
        if not results:
            print("  (no results)")
        for i, r in enumerate(results):
            print(f"  [{i+1}] {r['cmd_id']}/{r['section']} (score={r['score']:.4f})")
            print(f"       {r['text'][:120]}...")
            print()
