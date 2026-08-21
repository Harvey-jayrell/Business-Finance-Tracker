from flask import Flask
from app.config import get_database_url
from app.routes.health import health_bp
from app.extensions import db
from app.extensions import migrate
from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense
from app.models.investment import Investment
from app.models.investment_type import InvestmentType

def create_app(config_name):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] =get_database_url(config_name)
    db.init_app(app)
    migrate.init_app(app,db)
    app.register_blueprint(health_bp)

    return app