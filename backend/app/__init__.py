from flask import Flask
from app.config import get_database_url
from app.routes.health import health_bp
from app.extensions import db

def create_app(config_name):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] =get_database_url(config_name)
    db.init_app(app)
    app.register_blueprint(health_bp)

    return app