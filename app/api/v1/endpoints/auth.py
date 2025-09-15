from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.config import settings
from app.crud.user import create_user, get_user_by_email
from app.core.database import get_db

router = APIRouter()

@router.post("/register")
def register(user: dict, db: Session = Depends(get_db)):
    email = user.get("email")
    if not email or not user.get("password") or not user.get("first_name") or not user.get("last_name"):
        raise HTTPException(status_code=400, detail="Faltan campos requeridos")
    db_user = get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.get("password"))
    class _User:
        def __init__(self, data):
            self.email = data.get("email")
            self.first_name = data.get("first_name")
            self.last_name = data.get("last_name")
    db_user = create_user(db, _User(user), hashed_password)
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "is_active": db_user.is_active,
        "is_verified": db_user.is_verified,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at,
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}