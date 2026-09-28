from flask import Blueprint, request, jsonify, redirect, current_app
import sqlite3
from .db import get_db
from .utils import make_code
from .validators import validate_create_link

bp = Blueprint("views", __name__)

@bp.app_errorhandler(Exception)
def handle_unexpected(e):
    from werkzeug.exceptions import HTTPException
    if isinstance(e, HTTPException):
        raise e
    current_app.logger.exception("unexpected error")
    return jsonify({"error": "internal_error"}), 500

@bp.route("/links", methods=["POST"])
def create_link():
    data = request.get_json(silent=True)
    errors = validate_create_link(data)
    if errors:
        return jsonify({"error": "validation_failed", "fields": errors}), 400

    url = data["url"]
    db_path = current_app.config.get("DB_PATH")
    conn = get_db(db_path)
    existing = conn.execute("SELECT code FROM links WHERE url = ?", (url,)).fetchone()
    if existing is not None:
        code = existing["code"]
        conn.close()
        return jsonify({"code": code, "url": url}), 200
    code = make_code(url)
    try:
        conn.execute("INSERT INTO links (code, url) VALUES (?, ?)", (code, url))
        conn.commit()
    except sqlite3.IntegrityError:
        row = conn.execute("SELECT code FROM links WHERE url = ?", (url,)).fetchone()
        if row is not None:
            code = row["code"]
        else:
            code = make_code(url)
    finally:
        conn.close()
    return jsonify({"code": code, "url": url}), 201

@bp.route("/<code>")
def follow_link(code):
    db_path = current_app.config.get("DB_PATH")
    conn = get_db(db_path)
    row = conn.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({
            "error": "not_found",
            "fields": {"code": "no link with this code"}
        }), 404
    conn.execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))
    conn.commit()
    conn.close()
    return redirect(row["url"], code=302)

@bp.route("/links/<code>/stats")
def link_stats(code):
    db_path = current_app.config.get("DB_PATH")
    conn = get_db(db_path)
    row = conn.execute("SELECT url, clicks FROM links WHERE code = ?", (code,)).fetchone()
    conn.close()

    if row is None:
        return jsonify({
            "error": "not_found",
            "fields": {"code": "no link with this code"}
        }), 404
    return jsonify({"code": code, "url": row["url"], "clicks": row["clicks"]})
