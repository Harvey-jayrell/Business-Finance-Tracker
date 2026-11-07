from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
from app.extensions import db


health_bp = Blueprint("health", __name__)

@health_bp.route("/api/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "database": "connected"})
    
    except Exception:
        current_app.logger.exception("Database health check failed")
        return jsonify({"status": "down", "database": "disconnected"}), 503