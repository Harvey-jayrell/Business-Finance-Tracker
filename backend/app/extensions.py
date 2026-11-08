from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask import jsonify

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def register_error_handlers(app):
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"error":"The request body is not valid JSON"}), 400
    @app.errorhandler(415)
    def handle_unsupported_media_type(e):
        return jsonify({"error":"The request Content-Type was not application/json"}), 415
