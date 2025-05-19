# -*- encoding: utf-8 -*-

from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_user_type
from app.schemas.wedding import Wedding, WeddingCreate, WeddingUpdate
from app.models.models import User, Guest as GuestUserModel
from app.routers.router_wedding.router_wedding import (
    CreateWeddingController,
    GetWeddingByFianceController,
    GetWeddingController,
    UpdateWeddingController,
    DeleteWeddingController,
)
from app.schemas.user import GuestResponse
from typing import Any

router = APIRouter(
    prefix="/weddings",
    tags=["weddings"],
)

def get_router():
    return router

@router.post("/", response_model=Wedding, status_code=status.HTTP_201_CREATED)
def create_wedding(
    wedding: WeddingCreate = Body(...), 
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance"))
):
    return CreateWeddingController(session=session, wedding=wedding, current_user=current_user).execute()

@router.get("/{wedding_id}", response_model=Wedding)
def get_wedding(
    wedding_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance"))
):
    return GetWeddingController(session=session, wedding_id=wedding_id).execute()

@router.get("/fiance/{fiance_id}", response_model=Wedding)
def get_wedding_by_fiance(
    fiance_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance"))
):
    return GetWeddingByFianceController(session=session, fiance_id=fiance_id).execute()

@router.put("/{wedding_id}", response_model=Wedding)
def update_wedding(
    wedding_id: int,
    wedding: WeddingUpdate = Body(...),
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance"))
):
    return UpdateWeddingController(session=session, wedding_id=wedding_id, wedding=wedding).execute()

@router.delete("/{wedding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wedding(
    wedding_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance"))
):
    return DeleteWeddingController(session=session, wedding_id=wedding_id, current_user=current_user).execute()
