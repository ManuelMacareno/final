from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date
from uuid import UUID

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def create_expense(db: Session, expense_in: ExpenseCreate, user_id: UUID) -> Expense:
    expense = Expense(**expense_in.model_dump(), user_id=user_id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses(db: Session, user_id: UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_expense(db: Session, expense_id: UUID, user_id: UUID):
    return (
        db.query(Expense)
        .filter(and_(Expense.id == expense_id, Expense.user_id == user_id))
        .first()
    )


def update_expense(db: Session, expense_id: UUID, expense_in: ExpenseUpdate):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return None
    data = expense_in.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(expense, key, value)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: UUID):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        db.delete(expense)
        db.commit()


def get_expenses_by_date_range(db: Session, user_id: UUID, start_date: date, end_date: date):
    return (
        db.query(Expense)
        .filter(
            and_(
                Expense.user_id == user_id,
                Expense.date >= start_date,
                Expense.date <= end_date,
            )
        )
        .all()
    )


