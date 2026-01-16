import os
import subprocess
from flask import Blueprint, request, jsonify

admin_bp = Blueprint("admin", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "../uploads/bennett")
SCRIPT_DIR = os.path.join(BASE_DIR, "../scripts")

os.makedirs(UPLOAD_DIR, exist_ok=True)

ADMIN_PASSWORD = "admin123"


@admin_bp.route("/upload", methods=["POST"])
def upload_pdf():
    password = request.form.get("password")
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403

    file = request.files.get("file")
    if not file or not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Invalid file"}), 400

    save_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(save_path)

    return jsonify({"message": "PDF uploaded successfully"})


@admin_bp.route("/reindex", methods=["POST"])
def reindex():
    data = request.get_json()
    if not data or data.get("password") != ADMIN_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403

    subprocess.run(["python3", os.path.join(SCRIPT_DIR, "pdf_to_text.py")])
    subprocess.run(["python3", os.path.join(SCRIPT_DIR, "chunk_text.py")])

    return jsonify({"message": "Re-indexing completed"})
from analytics import get_top_questions

@admin_bp.route("/analytics", methods=["GET"])
def analytics():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return jsonify({"error": "Unauthorized"}), 403

    top = get_top_questions()
    return jsonify({
        "top_questions": [
            {"question": q, "count": c} for q, c in top
        ]
    })
