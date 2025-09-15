from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.crud.expense import (
    create_expense, get_expenses, get_expense, update_expense, delete_expense,
    get_expenses_by_date_range
)
from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ExpenseResponse)
def create_new_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return create_expense(db, expense, current_user.id)

@router.get("/", response_model=List[ExpenseResponse])
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if start_date and end_date:
        return get_expenses_by_date_range(db, current_user.id, start_date, end_date)
    elif category_id:
        # Filtro por categoría no implementado aún
        raise HTTPException(status_code=400, detail="Filtro por categoría no disponible")
    else:
        return get_expenses(db, current_user.id, skip, limit)

@router.get("/{expense_id}", response_model=ExpenseResponse)
def read_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    expense = get_expense(db, expense_id, current_user.id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_existing_expense(
    expense_id: UUID,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_expense = get_expense(db, expense_id, current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return update_expense(db, expense_id, expense)

@router.delete("/{expense_id}")
def delete_existing_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    expense = get_expense(db, expense_id, current_user.id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    delete_expense(db, expense_id)
    return {"message": "Expense deleted successfully"}