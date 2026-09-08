from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.category import Category
from app.auth_utils import permission_check

categories_bp = Blueprint("category", __name__)

@categories_bp.route("/api/categories", methods=["POST"])
@permission_check(["owner", "manager"])

def create_category():

    data = request.get_json()

    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"error": "name and description is required"}), 400

    name = name.title()

    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({"error": "Name must be unique"}), 409

    category = Category(
        name = name,
        description = description,

    )
    db.session.add(category)
    db.session.commit()

    return jsonify({
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "created_at": category.created_at,
        "updated_at": category.updated_at
    }), 201
