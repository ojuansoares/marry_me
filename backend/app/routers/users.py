# -*- encoding: utf-8 -*-

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.routers.users.user_controller import (
    CreateUserController,
    ListUsersController,
    GetUserController,
    UpdateUserController,
    DeleteUserController
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with the following information:
    - **nome**: Nome completo do usuário
    - **email**: Email único do usuário
    - **senha**: Senha do usuário
    - **telefone**: Número de telefone (opcional)
    - **tipo**: Tipo do usuário ('noivo' ou 'convidado')
    """
    return CreateUserController.execute(db=db, user=user)

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve users with pagination:
    - **skip**: Number of users to skip
    - **limit**: Maximum number of users to return
    """
    return ListUsersController.execute(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID
    """
    return GetUserController.execute(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user's information
    """
    return UpdateUserController.execute(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user
    """
    DeleteUserController.execute(db=db, user_id=user_id)
    return None 