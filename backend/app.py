from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS

from search_engine import search
from admin import admin_bp
from analytics import log_question
from penalty import penalty_bp

import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)
app.secret_key = "uniassist-secret-key"
CORS(app)

# -----------------------------
# BLUEPRINTS
# -----------------------------
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(penalty_bp, url_prefix="/penalty")

# -----------------------------
# FRONTEND SERVING (🔥 FIX)
# -----------------------------
@app.route("/")
def serve_chat():
    return send_from_directory(FRONTEND_DIR, "chat.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(FRONTEND_DIR, path)

# -----------------------------
# QUERY EXPANSION
# -----------------------------
QUERY_EXPANSIONS = {
    "outpass": "day out pass leave out pass hostel permission",
    "attendance": "minimum attendance percentage eligibility",
    "hostel": "hostel rules discipline warden",
    "exam": "end term examination supplementary exam rules",
}

def expand_query(q):
    q = q.lower()
    for key, val in QUERY_EXPANSIONS.items():
        if key in q:
            q += " " + val
    return q

# -----------------------------
# UTILITIES
# -----------------------------
def extract_sentences(text, query):
    keywords = [w for w in query.split() if len(w) > 3]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s for s in sentences if any(k in s.lower() for k in keywords)][:6]

def highlight_numbers(text):
    return re.sub(
        r"(\b\d+%|\b\d+\s?(AM|PM)|\b\d+\s?years?)",
        r"<strong style='color:#38bdf8'>\1</strong>",
        text,
        flags=re.IGNORECASE
    )

# -----------------------------
# CHAT API
# -----------------------------
@app.route("/ask", methods=["POST"])
def ask():
    query = request.json.get("query", "").strip()
    if not query:
        return jsonify({"answer": "Please ask a valid question."})

    log_question(query)
    expanded = expand_query(query)
    results = search(expanded)

    if not results:
        return jsonify({"answer": "<strong>No official rule found.</strong>"})

    top = results[0]
    sentences = extract_sentences(top["text"], expanded)

    summary = highlight_numbers(sentences[0]) if sentences else "No summary found."
    bullets = "".join(
        f"<li>{highlight_numbers(s)}</li>" for s in sentences[1:4]
    )

    answer = f"""
    <strong>Summary</strong>
    <p>{summary}</p>
    <strong>Key Points</strong>
    <ul>{bullets}</ul>
    <div style="font-size:12px;color:#94a3b8;">
      Source: {top['source']}
    </div>
    """

    return jsonify({"answer": answer})

# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=6060)

