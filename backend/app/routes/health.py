from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db

health_bp = Blueprint("health", __name__)

@health_bp.route("/api/health")
def health():
	try:
		db.session.execute(text("SELECT 1"))
		return jsonify({"status": "ok", "database": "connected"})
	
	except Exception as e:
		print(e)
		return jsonify({"status": "down", "database": "disconnected"})



	