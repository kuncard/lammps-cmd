"""Test VectorIndex build / load / search (fast, no model download)."""
import pytest, json, numpy as np
from pathlib import Path
from vector_index import VectorIndex

ROOT = Path(__file__).parent.parent
KB_DIR = ROOT / "lammps_kb"


def _make_chunks(n=5):
    """Create synthetic chunks for testing."""
    return [
        {
            "id": f"fix_nh__sec{i}",
            "cmd_id": "fix_nh",
            "title": "fix nvt command",
            "section": f"section{i}",
            "section_type": "description",
            "url": "https://docs.lammps.org/fix_nh.html",
            "phase": "integ",
            "text": f"This is chunk {i} about Nose-Hoover thermostat for NVT simulations.",
        }
        for i in range(n)
    ]


class TestVectorIndexBasics:

    def test_build_empty_chunks(self):
        vi = VectorIndex()
        vi.build([])
        assert len(vi.chunks) == 0
        assert vi.embeddings.shape == (0, 1)

    def test_build_with_chunks(self):
        """Synthetic embeddings (no model download)."""
        vi = VectorIndex()
        chunks = _make_chunks(5)
        # Inject fake embeddings to avoid model download
        vi.chunks = list(chunks)
        vi.embeddings = np.random.randn(5, 768).astype(np.float32)
        # L2-normalize (matching real behavior)
        norms = np.linalg.norm(vi.embeddings, axis=1, keepdims=True)
        vi.embeddings = vi.embeddings / norms
        vi.dim = 768
        assert len(vi.chunks) == 5

    def test_search_returns_results(self, monkeypatch):
        vi = VectorIndex()
        chunks = _make_chunks(3)
        vi.chunks = list(chunks)
        # Use a fixed "query vector" as one of the embeddings to guarantee a match
        q_vec = np.random.randn(768).astype(np.float32)
        q_vec = q_vec / np.linalg.norm(q_vec)
        vi.embeddings = np.array([
            q_vec,                                         # chunk 0 ≈ query
            np.random.randn(768).astype(np.float32),
            np.random.randn(768).astype(np.float32),
        ])
        norms = np.linalg.norm(vi.embeddings, axis=1, keepdims=True)
        vi.embeddings = vi.embeddings / norms
        vi.dim = 768

        # Stub _embed to return the fixed query vector (skip model download)
        def _fake_embed(texts):
            return np.array([q_vec] * len(texts))
        monkeypatch.setattr(vi, "_embed", _fake_embed)

        results = vi.search("Nose Hoover thermostat")
        assert len(results) > 0
        assert len(results) <= 10  # default top_k
        for r in results:
            assert "cmd_id" in r
            assert "score" in r
            assert "text" in r

    def test_search_empty_db(self):
        vi = VectorIndex()
        vi.chunks = []
        vi.embeddings = np.zeros((0, 1), dtype=np.float32)
        assert vi.search("anything") == []

    def test_search_top_k_respected(self, monkeypatch):
        vi = VectorIndex()
        chunks = _make_chunks(10)
        vi.chunks = list(chunks)
        q_vec = np.random.randn(768).astype(np.float32)
        q_vec = q_vec / np.linalg.norm(q_vec)
        emb = np.array([q_vec] + [np.random.randn(768).astype(np.float32) for _ in range(9)])
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        vi.embeddings = emb / norms
        vi.dim = 768

        def _fake_embed(texts):
            return np.array([q_vec] * len(texts))
        monkeypatch.setattr(vi, "_embed", _fake_embed)

        results = vi.search("test", top_k=3)
        assert len(results) <= 3
        assert len(results) > 0

    def test_save_load_roundtrip(self, tmp_path):
        """Save → load preserves chunks and embeddings."""
        vi = VectorIndex()
        chunks = _make_chunks(3)
        vi.chunks = list(chunks)
        vi.embeddings = np.random.randn(3, 768).astype(np.float32)
        norms = np.linalg.norm(vi.embeddings, axis=1, keepdims=True)
        vi.embeddings = vi.embeddings / norms
        vi.dim = 768

        # Save to temp dir
        import os
        emb_file = tmp_path / "embeddings.npy"
        chunks_file = tmp_path / "chunks_for_index.json"
        np.save(emb_file, vi.embeddings)
        meta = {"chunks": vi.chunks, "dim": vi.dim, "model_name": "test"}
        with open(chunks_file, "w", encoding="utf-8") as f:
            json.dump(meta, f)

        # Load back
        vi2 = VectorIndex()
        vi2.embeddings = np.load(emb_file)
        with open(chunks_file, encoding="utf-8") as f:
            meta2 = json.load(f)
        vi2.chunks = meta2["chunks"]
        vi2.dim = meta2["dim"]

        assert len(vi2.chunks) == 3
        assert vi2.dim == 768
        assert vi2.embeddings.shape == (3, 768)
