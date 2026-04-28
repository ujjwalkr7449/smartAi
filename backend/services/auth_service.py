from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.security import create_token, hash_password, verify_password
from models.user import User


def register_user(db: Session, email: str, full_name: str, password: str, role):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(email=email, full_name=full_name, hashed_password=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str, access_ttl: int, refresh_ttl: int):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {
        "access_token": create_token(user.email, access_ttl, "access"),
        "refresh_token": create_token(user.email, refresh_ttl, "refresh"),
    }
