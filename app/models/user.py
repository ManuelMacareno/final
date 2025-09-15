from sqlalchemy import Column, String, Boolean, UUID, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<User {self.email}>"

    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")