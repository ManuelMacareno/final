from sqlalchemy import Column, String, Numeric, Date, Boolean, ForeignKey, UUID, Text
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255))
    receipt_url = Column(String(500))
    is_recurring = Column(Boolean, default=False)
    recurrence_frequency = Column(String(20))
    
    user = relationship("User", back_populates="expenses")