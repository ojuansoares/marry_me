from datetime import timedelta
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
    # Busca o usuário pelo email
    user = GetUserByEmailController.execute(db, u_email=form_data.username)
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
            "user_id": user.id,
            "user_type": user.u_type
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user.u_type
    }