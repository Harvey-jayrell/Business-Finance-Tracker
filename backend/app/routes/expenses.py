from flask import Blueprint, request, jsonify
from app.extensions import db
from app.auth_utils import get_current_user_id
from app.models.expense import Expense
from app.models.user import User
from app.extensions import bcrypt
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime


expense_bp = Blueprint("expense",__name__)

@expense_bp.route("/api/expenses", methods=["POST"])
@jwt_required()
def create_expense():

    data = request.get_json()
    user_id = get_current_user_id()

    title = data.get("title")
    amount = data.get("amount")
    expense_date = data.get("expense_date")
    notes = data.get("notes")
    category_id = data.get("category_id")


    if not title or not amount or not expense_date or not category_id:
        return jsonify({"error": "title, amount, expense_date and category_id is required"}),400
    if amount <= 0:
        return jsonify({"error":"the amount can't be valued as 0 or negative"}), 400    

    expense = Expense(
        user_id = user_id,
        title = title,
        amount = amount,
        expense_date = expense_date,
        notes = notes,
        category_id = category_id
        )
    db.session.add(expense)
    db.session.commit()

    return jsonify({
        "id": expense.id,
        "user_id": expense.user_id,
        "title": expense.title,
        "amount": expense.amount,
        "expense_date": expense.expense_date,
        "notes": expense.notes,
        "category_id": expense.category_id
    }),201

@expense_bp.route("/api/expenses", methods=["GET"])
@jwt_required()

def get_expenses():
    user_id = get_current_user_id()
    claims = get_jwt()
    role = claims.get("role")

    query = Expense.query
    query = query.filter_by(deleted_at=None)
    if role == "cashier":
        query = query.filter_by(user_id=user_id)
    results=query.all()
    expenses_list = []
    for expense in results:
        expenses_list.append({
            "id": expense.id,
            "user_id": expense.user_id,
            "title": expense.title,
            "amount": expense.amount,
            "expense_date": expense.expense_date,
            "notes": expense.notes,
            "category_id": expense.category_id,
    })
    return jsonify(expenses_list),200

@expense_bp.route("/api/expenses/<int:expense_id>", methods=["PATCH"])
@jwt_required()
def edit_expense(expense_id):
    user_id = get_current_user_id()
    claims = get_jwt()
    role = claims.get("role")

    if role not in ["owner", "manager", "cashier"]:
        return jsonify({"error": "Permission denied"}), 403

    expense = Expense.query.get(expense_id)
    if expense is None or expense.deleted_at is not None:
        return jsonify({"error": "Expense not found"}), 404

    if role == "cashier" and expense.user_id != user_id:
        return jsonify({"error":"Expense not found"}), 404

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    if "amount" in data:
        if not isinstance(data["amount"], (int, float)) or isinstance(data["amount"], bool):
            return jsonify({"error": "Amount must be a JSON number"}), 400
        if data["amount"] <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400

    if "title" in data:
        if not isinstance(data["title"], (str)):
            return jsonify({"error": "Title must be a JSON string"}), 400
        if not data["title"].strip():
            return jsonify({"error": "Title must not be blank"}), 400
        
    patchable_fields = ["title", "amount", "expense_date", "notes", "category_id"]
    for field in patchable_fields:
        if field in data:
            setattr(expense, field, data[field])
    db.session.commit()
    return jsonify({
        "id": expense.id,
        "user_id": expense.user_id,
        "title": expense.title,
        "amount": expense.amount,
        "expense_date": expense.expense_date,
        "notes": expense.notes,
        "category_id": expense.category_id,
    }), 200

@expense_bp.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_current_user_id()
    claims = get_jwt()
    role = claims.get("role")

    if role not in ["owner", "manager", "cashier"]:
        return jsonify({"error": "Permission denied"}), 403

    expense = Expense.query.get(expense_id)
    if expense is None or expense.deleted_at is not None:
        return jsonify({"error":"Expense not found"}), 404
    if role == "cashier":
        if expense.user_id != user_id:
            return jsonify({"error": "Expense not found"}), 404
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error":"Request body must be a JSON object"}), 400
        password = data.get("password")

        if password is None:
            return jsonify({"error": "Password required"}), 400
        
        if not isinstance(password, str):
            return jsonify({"error": "Password must be a string"}), 400

        user = User.query.get(user_id)
        password_valid = bcrypt.check_password_hash(user.password_hash, password)
        if not password_valid:
            return jsonify({"error":"Invalid credentials"}), 401
    expense.deleted_at = datetime.utcnow()
    expense.deleted_by = user_id
    db.session.commit()
    return jsonify({
        "id": expense.id,
        "deleted_at": expense.deleted_at,
        "deleted_by": expense.deleted_by
    }),200
