# app/services/analytics.py
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, and_
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

from app.models.expense import Expense

class AnalyticsService:
    @staticmethod
    def get_monthly_summary(db: Session, user_id: UUID, year: int, month: int):
        total_expenses = db.query(func.sum(Expense.amount)).filter(
            and_(
                Expense.user_id == user_id,
                extract('year', Expense.date) == year,
                extract('month', Expense.date) == month
            )
        ).scalar() or 0.0
        
        # Obtener gastos por categoría
        expenses_by_category = db.query(
            Expense.category_id,
            func.sum(Expense.amount).label('total')
        ).filter(
            and_(
                Expense.user_id == user_id,
                extract('year', Expense.date) == year,
                extract('month', Expense.date) == month
            )
        ).group_by(Expense.category_id).all()
        
        return {
            'total_expenses': float(total_expenses),
            'expenses_by_category': [
                {'category_id': cat_id, 'total': float(total)}
                for cat_id, total in expenses_by_category
            ]
        }
    
    @staticmethod
    def get_budget_vs_actual(db: Session, user_id: UUID, month: int, year: int):
        # Placeholder: no hay modelo Budget definido
        return {"budget": 0.0, "actual": 0.0}
    
    @staticmethod
    def get_spending_trends(db: Session, user_id: UUID, months: int = 6):
        # Placeholder de tendencias
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=30 * months)
        total = db.query(func.sum(Expense.amount)).filter(
            and_(Expense.user_id == user_id, Expense.date >= start_date, Expense.date <= end_date)
        ).scalar() or 0.0
        return {"from": start_date.isoformat(), "to": end_date.isoformat(), "total": float(total)}