"""
Flask API server for LAMMPS Manual retrieval.
Startup loads BM25 + vector indexes → ready for queries.

Usage:
  python app.py             # start server at http://localhost:5000
  python app.py --port 8761 # custom port
  python app.py --rebuild   # rebuild indexes before starting
"""
import sys, argparse, json
from pathlib import Path

from logging_setup import setup_logging
log = setup_logging("lammps-cmd")

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from flask import Flask, request, jsonify, send_from_directory
from hybrid_search import HybridRetriever
from bm25_index import BM25Index, build_from_kb, classify_query, tokenize
from vector_index import VectorIndex
from query_expander import QueryExpander

app = Flask(__name__)
retriever = None

# Lazy-loaded QueryExpander (built from graph_data_full.json)
_expander = None


def _get_expander():
    """Lazy-load QueryExpander from graph data. Returns None if graph unavailable."""
    global _expander
    if _expander is not None:
        return _expander
    graph_file = ROOT / "graph_data_full.json"
    if graph_file.exists():
        with open(graph_file, encoding="utf-8") as f:
            g = json.load(f)
        _expander = QueryExpander(g["nodes"])
        log.info("QueryExpander loaded from graph_data_full.json")
    return _expander


def build_indexes():
    """Rebuild BM25 and vector indexes from lammps_kb/."""
    log.info("Building indexes...")
    chunks = build_from_kb()

    bm25 = BM25Index()
    bm25.build(chunks)
    bm25.save()

    vec = VectorIndex()
    vec.build(chunks)
    vec.save()

    return HybridRetriever(bm25, vec, expander=_get_expander())


def load_indexes(skip_vector=False):
    """Load existing indexes, or build if missing."""
    bm25_idx = ROOT / "lammps_kb" / "bm25_index.json"
    emb_file = ROOT / "lammps_kb" / "embeddings.npy"

    bm25 = BM25Index()
    if bm25_idx.exists():
        bm25.load()
    else:
        log.info("BM25 index not found, building...")
        chunks = build_from_kb()
        bm25.build(chunks)
        bm25.save()

    expander = _get_expander()

    if skip_vector:
        log.info("Vector search disabled (--skip-vector). BM25-only mode.")
        return HybridRetriever(bm25, None, expander=expander)

    if emb_file.exists():
        vec = VectorIndex()
        if vec.load():
            return HybridRetriever(bm25, vec, expander=expander)

    log.warning("Vector index not found. Run 'python vector_index.py --build' to enable semantic search.")
    log.warning("Starting in BM25-only mode.")
    return HybridRetriever(bm25, None, expander=expander)


@app.route("/")
def index():
    return send_from_directory(str(ROOT), "index.html")

@app.route("/graph")
def graph():
    return send_from_directory(str(ROOT), "graph.html")

@app.route("/<path:filename>")
def static_files(filename):
    """Serve graph_data.json, lammps_kb/*.md, and other static files."""
    filepath = ROOT / filename
    if filepath.exists():
        return send_from_directory(str(ROOT), filename)
    return "Not found", 404


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "indexes_loaded": retriever is not None})


@app.route("/api/search", methods=["POST"])
def search():
    """Retrieval-only endpoint. Returns top-k document chunks with scores."""
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "invalid JSON body"}), 400

    question = (data.get("question") or "").strip()
    raw_top_k = data.get("top_k", 5)

    # ── Validate ──
    if not question:
        return jsonify({"error": "question is required"}), 400
    if len(question) > 500:
        return jsonify({"error": "question too long (max 500 chars)"}), 400

    try:
        top_k = int(raw_top_k)
    except (TypeError, ValueError):
        return jsonify({"error": "top_k must be an integer"}), 400
    top_k = max(1, min(50, top_k))  # clamp to [1, 50]

    if retriever is None:
        return jsonify({"error": "Index not loaded"}), 500

    qtype, qparams = classify_query(question)

    vec_k = int(top_k * 4 * qparams["vec_weight"])
    bm25_k = int(top_k * 4 * qparams["bm25_weight"])

    results = retriever.search(
        question, top_k=top_k,
        per_index=max(bm25_k, vec_k),
        query_type=qtype
    )
    return jsonify({
        "question": question,
        "query_type": qtype,
        "query_tokens": tokenize(question),
        "results": results
    })


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--host", default="127.0.0.1",
                    help="Bind address (default: 127.0.0.1; use 0.0.0.0 to expose on LAN)")
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--skip-vector", action="store_true",
                    help="Skip vector search (BM25-only, no model download needed)")
    args = ap.parse_args()

    if args.rebuild:
        retriever = build_indexes()
    else:
        retriever = load_indexes(skip_vector=args.skip_vector)

    mode = "BM25-only" if args.skip_vector else "BM25 + Vector"
    log.info("LAMMPS Manual Search (%s) starting at http://%s:%s", mode, args.host, args.port)
    # Use waitress if available (production), fall back to Flask dev server
    try:
        from waitress import serve
        log.info("Using waitress production server")
        serve(app, host=args.host, port=args.port)
    except ImportError:
        log.info("Using Flask dev server (install waitress for production)")
        app.run(host=args.host, port=args.port, debug=False)
