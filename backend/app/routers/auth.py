from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
)
from app.core.config import settings
from app.routers.router_user.router_user import GetUserByEmailController
from app.schemas.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = GetUserByEmailController(db, u_email=form_data.username).execute()
    if not user or not verify_password(form_data.password, user.u_password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cria o token de acesso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.u_email,
            "user_type": user.u_type,
            "user_email": user.u_email,
            "user_id": user.id
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.u_type,
        "user_email": user.u_email,
        "user_id": user.id
    }

@router.get("/test")
def test_connection():
    print("Test endpoint called!")  # Log no console do backend
    return {
        "status": "ok", 
        "message": "Backend is running!",
        "timestamp": datetime.now().isoformat()
    }