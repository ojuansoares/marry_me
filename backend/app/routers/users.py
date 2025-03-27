# -*- encoding: utf-8 -*-

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.routers.router_user.router_user import (
    CreateUserController,
    GetUserController,
    UpdateUserController,
    DeleteUserController
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def get_router():
    return router

@router.post(
    "/", 
    response_model=User, 
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate = Query(), 
    db: Session = Depends(get_db)
):
    return CreateUserController(db=db, user=user).execute()

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return GetUserController.execute(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return UpdateUserController.execute(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    DeleteUserController.execute(db=db, user_id=user_id)
    return None 