"""Test Flask API endpoints (integration)."""
import pytest, json, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from app import app as flask_app


@pytest.fixture
def client():
    """Flask test client with BM25-only mode (fast, no model download)."""
    from app import load_indexes, retriever as _global_retriever
    import app as app_module

    # Load indexes once if not already loaded
    if app_module.retriever is None:
        app_module.retriever = load_indexes(skip_vector=True)

    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


class TestHealth:
    def test_health_returns_ok(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data["status"] == "ok"
        assert data["indexes_loaded"] is True


class TestSearch:
    def test_search_requires_question(self, client):
        resp = client.post("/api/search",
                           data=json.dumps({}),
                           content_type="application/json")
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert "error" in data

    def test_search_empty_question(self, client):
        resp = client.post("/api/search",
                           data=json.dumps({"question": "  "}),
                           content_type="application/json")
        assert resp.status_code == 400

    def test_search_returns_results(self, client):
        resp = client.post("/api/search",
                           data=json.dumps({"question": "fix nvt", "top_k": 3}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert "results" in data
        assert "question" in data
        assert "query_type" in data
        assert data["question"] == "fix nvt"
        assert len(data["results"]) > 0
        assert len(data["results"]) <= 3

    def test_search_result_structure(self, client):
        resp = client.post("/api/search",
                           data=json.dumps({"question": "compute temp"}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        for r in data["results"]:
            assert "cmd_id" in r
            assert "title" in r
            assert "text" in r
            assert "url" in r
            assert "rrf_score" in r

    def test_search_top_k_respected(self, client):
        resp = client.post("/api/search",
                           data=json.dumps({"question": "velocity", "top_k": 2}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data["results"]) <= 2

    def test_search_handles_special_chars(self, client):
        """Queries with special characters should not 500."""
        resp = client.post("/api/search",
                           data=json.dumps({"question": "lj/cut 10.0"}),
                           content_type="application/json")
        assert resp.status_code == 200

    def test_search_rejects_invalid_json(self, client):
        resp = client.post("/api/search",
                           data="not json",
                           content_type="application/json")
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert "error" in data

    def test_search_rejects_long_question(self, client):
        resp = client.post("/api/search",
                           data=json.dumps({"question": "x" * 501}),
                           content_type="application/json")
        assert resp.status_code == 400

    def test_search_clamps_top_k(self, client):
        """top_k=999 should be clamped to 50, top_k=-5 to 1."""
        resp = client.post("/api/search",
                           data=json.dumps({"question": "velocity", "top_k": 999}),
                           content_type="application/json")
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert len(data["results"]) <= 50

    def test_search_rejects_non_integer_top_k(self, client):
        resp = client.post("/api/search",
                           data=json.dumps({"question": "velocity", "top_k": "abc"}),
                           content_type="application/json")
        assert resp.status_code == 400


class TestStaticPages:
    def test_index_page(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"LAMMPS Manual Search" in resp.data

    def test_graph_page(self, client):
        resp = client.get("/graph")
        assert resp.status_code == 200
