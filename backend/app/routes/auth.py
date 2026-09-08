from flask import Blueprint, request, jsonify
from app.extensions import db, bcrypt
from app.models.user import User
from flask_jwt_extended import create_access_token
from app.auth_utils import owner_required

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
            access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
            return jsonify({
                "access_token": access_token,
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }), 200

@auth_bp.route("/api/users", methods=["POST"])
@owner_required
def create_employee():

    data = request.get_json()

    name= data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not name or not email or not password or not role:
        return jsonify({"error": "Name, Email, Password, and role are required"}), 400

    if role not in ["manager", "cashier"]:
        return jsonify({"error": "Invalid role"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Email already registered"}), 409


    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        name=name,
        email=email,
        password_hash=hashed_password,
        role=role
        )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }), 201


