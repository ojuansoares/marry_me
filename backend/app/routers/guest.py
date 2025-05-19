# -*- encoding: utf-8 -*-

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import User, UserCreate
from app.schemas.guest import CreateWeddingGuest, Invite, GuestResponse
from app.schemas.wedding import Wedding
from app.routers.router_guest.router_guest import (
    CreateWeddingGuestController,
    CreateGuestUserController,
    ValidateGuestByPhoneController,
    GetPendingInvitesController,
    AcceptInvite,
    DeclineInvite,
    GetWeddingGuests,
    GetWeddingsByGuestController,
)
from app.core.security import get_current_user, require_user_type

router = APIRouter(
    prefix="/guest",
    tags=["guest"],
)

def get_router():
    return router

@router.get("/wedding_guests", response_model=list[GuestResponse])
def get_wedding_guests(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("fiance"))
):
    current_user_id = current_user.id if isinstance(current_user.id, int) else current_user.id.value
    return GetWeddingGuests(session=session, fiance_id=current_user_id).execute()

@router.get("/guest", response_model=list[Wedding])
def get_wedding_by_guest(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: bool = Depends(require_user_type("guest"))
):
    guest_id = current_user.id if isinstance(current_user.id, int) else current_user.id.value
    return GetWeddingsByGuestController(session, guest_id).execute()

@router.get("/validate_guest_by_phone" , response_model=bool)
def validate_guest_by_phone(
    phone: str,
    session: Session = Depends(get_db),
):
    return ValidateGuestByPhoneController(session, phone).execute()

@router.get("/pending_invites", response_model=list[Invite])
async def read_pending_invites(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
    _: bool = Depends(require_user_type("guest")),
):
    current_user_id = current_user.id if isinstance(current_user.id, int) else current_user.id.value
    return GetPendingInvitesController(session, current_user_id).execute()

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