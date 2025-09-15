# app/services/notifications.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from app.models.expense import Expense

def check_budget_alerts(db: Session):
    # Placeholder sin modelo Budget ni servicio de email
    return True

def send_weekly_report(db: Session, user_id: str):
    # Placeholder sin servicio de email
    return True