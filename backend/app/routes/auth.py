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

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Invalid Credentials"}), 401
    else:
        check_password = bcrypt.check_password_hash(user.password_hash, password)
        if check_password is False:
            return jsonify({"error": "Invalid Credentials"}), 401
        else:
            return jsonify({"id": user.id, "name": user.name, "email": user.email, "role": user.role}), 200
