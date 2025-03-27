# -*- encoding: utf-8 -*-

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.routers.router_user.router_user import (
    CreateUserController,
    GetUserController,
    UpdateUserController,
    DeleteUserController
)

router = APIRouter(
    prefix="/weddings",
    tags=["weddings"],
)

def get_router():
    return router

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate = Query(), 
    session: Session = Depends(get_db)
):
    return CreateUserController(session=session, user=user).execute()