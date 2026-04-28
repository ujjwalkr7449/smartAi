from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.config import settings
from core.security import create_token, decode_token
from db.session import get_db
from schemas.auth import LoginRequest, RefreshTokenRequest, RegisterRequest, TokenResponse, UserResponse
from services.auth_service import login_user, register_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, payload.email, payload.full_name, payload.password, payload.role)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, payload.email, payload.password, settings.access_token_exp_minutes, settings.refresh_token_exp_minutes)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest):
    data = decode_token(payload.refresh_token)
    if data.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    email = data["sub"]
    return {
        "access_token": create_token(email, settings.access_token_exp_minutes, "access"),
        "refresh_token": payload.refresh_token,
        "token_type": "bearer",
    }
