from flask import Flask
from app.config import get_database_url
from app.config import get_jwt_secret_key
from app.routes.health import health_bp
from app.routes.expenses import expense_bp
from app.routes.categories import categories_bp
from app.extensions import db
from app.extensions import migrate
from app.extensions import bcrypt
from app.extensions import jwt
from app.extensions import register_error_handlers
from app.routes.auth import auth_bp
from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense
from app.models.investment import Investment
from app.models.investment_type import InvestmentType

def create_app(config_name):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] =get_database_url(config_name)
    app.config["JWT_SECRET_KEY"] = get_jwt_secret_key()
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    register_error_handlers(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(categories_bp)

    return app
