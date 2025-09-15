from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID

from app.models.user import User


def get_user_by_email(db: Session, email: str):
    if not email:
        return None
    return db.query(User).filter(func.lower(User.email) == email.lower()).first()


def create_user(db: Session, user_in, hashed_password: str) -> User:
    user = User(
        email=(user_in.email or "").lower(),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


