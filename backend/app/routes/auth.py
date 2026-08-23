from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.count() > 0:
        return jsonify({"error": "Registration is closed"}), 403

    

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(name=name, email=email, password_hash=hashed_password, role="owner")

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"id": new_user.id, "name": new_user.name, "email": new_user.email, "role": new_user.role}), 201