# -*- encoding: utf-8 -*-

from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.routers.router_user.router_user import (
    CreateUserController,
    GetUserController,
    UpdateUserController,
    DeleteUserController
)
from app.core.security import get_current_user, require_user_type

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

def get_router():
    return router

@router.post("/", response_model=User)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_db)
):
    return CreateUserController(session=session, user=user).execute()

@router.get("/me", response_model=User)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """Get current user's information"""
    return current_user

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance")),  # Verifica se é fiance
    session: Session = Depends(get_db)
):
    """Get user information by ID (only accessible by fiance users)"""
    # Verifica se o usuário está tentando acessar seus próprios dados
    if current_user.id == user_id:
        return current_user
        
    return GetUserController.execute(session=session, user_id=user_id)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_db)):
    return UpdateUserController.execute(session=session, user_id=user_id, user=user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_db)):
    DeleteUserController.execute(session=session, user_id=user_id)
    return None 