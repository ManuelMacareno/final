from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class ExpenseBase(BaseModel):
    amount: float
    description: str
    date: date
    location: Optional[str] = None
    receipt_url: Optional[str] = None
    is_recurring: bool = False
    recurrence_frequency: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[date] = None
    location: Optional[str] = None
    receipt_url: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_frequency: Optional[str] = None


class ExpenseInDB(ExpenseBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExpenseResponse(ExpenseInDB):
    pass


