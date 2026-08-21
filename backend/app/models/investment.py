from app.extensions import db
from datetime import datetime
from datetime import date

class Investment(db.Model):
    __tablename__ = "investments"

    id = db.Column(db.Integer, primary_key=True)
    requested_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    investment_type_id = db.Column(db.Integer, db.ForeignKey("investment_types.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    current_value = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String, nullable=True)
    investment_date = db.Column(db.Date, default= date.today)
    status = db.Column(db.String, nullable=False)
    decided_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    decision_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)


    __table_args__ = (
        db.CheckConstraint("status IN ('pending', 'approved', 'rejected')", name="check_valid_status"),
    )