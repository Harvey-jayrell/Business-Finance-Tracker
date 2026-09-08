from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.expense import Expense
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


expense_bp = Blueprint("expense",__name__)

@expense_bp.route("/api/expenses", methods=["POST"])
@jwt_required()
def create_expense():

    data = request.get_json()
    user_id = get_jwt_identity()

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
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")

    query = Expense.query
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
        