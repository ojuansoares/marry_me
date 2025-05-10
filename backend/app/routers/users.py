# -*- encoding: utf-8 -*-

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate, CreateWeddingGuest
from app.schemas.wedding import Invite
from app.routers.router_user.router_user import (
    CreateUserController,
    GetUserController,
    UpdateUserController,
    DeleteUserController,
    CreateWeddingGuestController,
    CreateGuestUserController,
    ValidateGuestByPhoneController,
    GetPendingInvitesController,
    AcceptInvite,
    DeclineInvite,
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

@router.get("/validate_guest_by_phone" , response_model=bool)
def validate_guest_by_phone(
    phone: str,
    session: Session = Depends(get_db),
):
    return ValidateGuestByPhoneController(session, phone).execute()

@router.get("/me", response_model=User)
async def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """Get current user's information"""
    return current_user

@router.get("/pending_invites", response_model=list[Invite])
async def read_pending_invites(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
    _: bool = Depends(require_user_type("guest")),
):
    current_user_id = current_user.id if isinstance(current_user.id, int) else current_user.id.value
    return GetPendingInvitesController(session, current_user_id).execute()

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance")),  # Verifica se é fiance
    session: Session = Depends(get_db)
):
    if current_user.id == user_id:
        return current_user

    return GetUserController(session=session, user_id=user_id).execute()

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UpdateUserController(session=session, user_id=user_id, user=user).execute()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int, 
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DeleteUserController(session=session, user_id=user_id).execute()

@router.post("/wedding_guest", response_model=str)
def create_wedding_guest(
    params: CreateWeddingGuest,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance")),
):
    return CreateWeddingGuestController(session, params, current_user).execute()

@router.post("/guest", response_model=User)
def create_guest_user(
    user: UserCreate,
    session: Session = Depends(get_db)
):
    return CreateGuestUserController(session, user).execute()

@router.post("/accept_invite", status_code=status.HTTP_204_NO_CONTENT)
def accept_invite(
    guest_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("guest")),
):
    return AcceptInvite(session=session, guest_id=guest_id).execute()

@router.post("/decline_invite", status_code=status.HTTP_204_NO_CONTENT)
def decline_invite(
    guest_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("guest")),
):
    return DeclineInvite(session=session, guest_id=guest_id).execute()