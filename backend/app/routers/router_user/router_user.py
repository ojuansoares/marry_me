# -*- encoding: utf-8 -*-

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate, UserUpdate, UserInDB, CreateWeddingGuest
from app.schemas.wedding import Invite
from app.models.models import User as UserModel, Guest as GuestUserModel, Wedding as WeddingModel
from app.core.security import get_password_hash
from app.services.user_service import get_user_by_email
from app.schemas.constants import Group
from sqlalchemy import func
from datetime import datetime


class CreateUserController:
    def __init__(self, session: Session, user: UserCreate) -> None:
        self._session = session
        self._user = user

    def execute(self) -> User:
        try:
            db_user = get_user_by_email(self._session, self._user.u_email)
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user = self.create_user()
            self._session.commit()
            return user
        except Exception as e:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def create_user(self) -> User:
        hashed_password = get_password_hash(self._user.u_password)
        db_user = UserModel(
            u_name=self._user.u_name,
            u_email=self._user.u_email,
            u_phone=self._user.u_phone,
            u_type=self._user.u_type,
            u_password_hash=hashed_password
        )
        self._session.add(db_user)
        self._session.flush()
        return User.from_orm(db_user)


class GetUserController:
    def __init__(self, session: Session, user_id: int):
        self._session = session
        self._user_id = user_id

    def execute(self) -> User:
        try:
            db_user = self._session.query(UserModel).filter(UserModel.id == self._user_id).first()
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return User.from_orm(db_user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

class GetUserByEmailController:
    def __init__(self, session: Session, u_email: str):
        self._session = session
        self._u_email = u_email

    
    def execute(self) -> UserInDB | None:
        user = self._session.query(UserModel).filter(UserModel.u_email == self._u_email).first()
        formated_user = UserInDB.from_orm(user) if user else None
        return formated_user

class UpdateUserController:
    def __init__(self, session: Session, user_id: int, user: UserUpdate):
        self._session = session
        self._user_id = user_id
        self._user = user

    def execute(self) -> User:
        try:
            db_user = self._session.query(UserModel).filter(UserModel.id == self._user_id).first()
            if not db_user:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            update_data = self._user.dict(exclude_unset=True)
            if "u_password" in update_data:
                update_data["u_password_hash"] = get_password_hash(update_data.pop("u_password"))

            for field, value in update_data.items():
                setattr(db_user, field, value)

            self._session.commit()
            self._session.refresh(db_user)
            return User.from_orm(db_user)
        except Exception as e:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )


class DeleteUserController:
    def __init__(self, session: Session, user_id: int):
        self._session = session
        self._user_id = user_id
    
    def execute(self) -> None:
        try:
            db_user = self._session.query(UserModel).filter(UserModel.id == self._user_id).first()
            if not db_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            self._session.delete(db_user)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

class CreateWeddingGuestController:
    def __init__(self, session: Session, params: CreateWeddingGuest, current_user: User):
        self._session = session
        self._params = params
        self._current_user = current_user

    def execute(self) -> str | None:
        try:
            self.create_guest_user()
            self._session.commit()
            return "Guest user created successfully"
        except Exception as e:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def create_guest_user(self) -> None:
        guest_user = GuestUserModel(
            g_name=self._params.g_name,
            g_phone=self._params.g_phone,
            g_group_id=self._params.g_group_id if self._params.g_group_id else None,
            g_responsible_id=self._params.g_responsible_id if self._params.g_responsible_id else None,
        )
        wedding_id = self._session.query(WeddingModel).filter(WeddingModel.w_fiance_id == self._current_user.id).first()
        if not wedding_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wedding not found"
            )
        guest_user.g_wedding_id = wedding_id.id
        
        if guest_user.g_group_id is not None and guest_user.g_responsible_id is not None:
            group = next((g for g in Group.ALL_GROUPS if g["id"] == guest_user.g_group_id), None)
            if not group:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid group ID"
                )
            group_limit = group["limit"]
            guest_count = self._session.query(func.count(GuestUserModel.id)).filter(
                GuestUserModel.g_group_id == guest_user.g_group_id,
                GuestUserModel.g_responsible_id == guest_user.g_responsible_id
            ).scalar()

            if guest_count >= group_limit:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"The group '{group['name']}' has reached its limit of {group_limit} members"
                )
        
        self._session.add(guest_user)
        self._session.flush()


class CreateGuestUserController:
    def __init__(self, session: Session, user: UserCreate) -> None:
        self._session = session
        self._user = user
        self._new_guest_user = GuestUserModel()

    def execute(self) -> User:
        try:
            db_user = get_user_by_email(self._session, self._user.u_email)
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user = self.create_user()
            self._session.commit()
            return user
        except Exception as e:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def validate_guest(self) -> bool | None:
        if self._user.u_phone is not None:
            db_user = self._session.query(GuestUserModel).filter(GuestUserModel.g_phone == self._user.u_phone).first()
            return True if db_user else False
        return None
    
    def update_guest(self) -> None:
        if self._user.u_phone is not None:
            db_user = self._session.query(GuestUserModel).filter(GuestUserModel.g_phone == self._user.u_phone).first()
            if db_user and self._new_guest_user:
                db_user.g_user_id = self._new_guest_user.id

    def create_user(self) -> User:
        hashed_password = get_password_hash(self._user.u_password)
        self._new_guest_user = UserModel(
            u_name=self._user.u_name,
            u_email=self._user.u_email,
            u_phone=self._user.u_phone,
            u_type=self._user.u_type,
            u_password_hash=hashed_password
        )
        guest_validated = self.validate_guest()
        if not guest_validated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not a guest"
            )

        self._session.add(self._new_guest_user)
        self._session.flush()
        self.update_guest()
        return User.from_orm(self._new_guest_user)


class ValidateGuestByPhoneController:
    def __init__(self, session: Session, phone: str) -> None:
        self._session = session
        self._phone = phone

    def execute(self) -> bool:
        try:
            validated_guest = self.validate_guest()
            if not validated_guest:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Guest not found"
                )
            return True if validated_guest else False
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def validate_guest(self) -> bool | None:
        if self._phone is not None:
            db_user = self._session.query(GuestUserModel).filter(GuestUserModel.g_phone == self._phone).first()
            return True if db_user else False
        return None


class GetPendingInvitesController:
    def __init__(self, session: Session, guest_id: int) -> None:
        self._session = session
        self._guest_id = guest_id

    def execute(self) -> list[Invite]:
        try:
            pending_invites = self.get_pending_invites()
            if not pending_invites:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No pending invites found"
                )
            return pending_invites
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def get_pending_invites(self) -> list[Invite]:
        pending_wedding_data = (
            self._session.query(GuestUserModel.g_wedding_id, GuestUserModel.id)
            .filter(
                GuestUserModel.g_user_id == self._guest_id,
                GuestUserModel.g_confirmed == False
            )
            .all()
        )
        wedding_to_guest_map = {wedding_id: g_id for wedding_id, g_id in pending_wedding_data}
        wedding_ids = list(wedding_to_guest_map.keys())
        if not wedding_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No pending invites found for this guest"
            )

        weddings = (
            self._session.query(WeddingModel)
            .filter(WeddingModel.id.in_(wedding_ids))
            .all()
        )
        if not weddings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No weddings found"
            )

        return [
            Invite(
                w_id=wedding.id if isinstance(wedding.id, int) else wedding.id.value,
                w_date=wedding.w_date if isinstance(wedding.w_date, datetime) else datetime.strptime(str(wedding.w_date), "%Y-%m-%d"),
                w_fiance_name=str(wedding.w_fiance_name),
                w_bride_name=str(wedding.w_bride_name),
                w_location=str(wedding.w_location),
                w_description=str(wedding.w_description),
                g_id=wedding_to_guest_map[wedding.id]
            )
            for wedding in weddings
        ]

class AcceptInvite:
    def __init__(self, session: Session, guest_id: int) -> None:
        self._session = session
        self._guest_id = guest_id

    def execute(self) -> None:
        try:
            guest = self._session.query(GuestUserModel).filter(GuestUserModel.id == self._guest_id).first()
            if not guest:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Guest not found"
                )
            guest.g_confirmed = True  # type: ignore

            responsible_guests = self._session.query(GuestUserModel).filter(GuestUserModel.g_responsible_id == self._guest_id).all()
            for responsible_guest in responsible_guests:
                responsible_guest.g_confirmed = True  # type: ignore

            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

class DeclineInvite:
    def __init__(self, session: Session, guest_id: int) -> None:
        self._session = session
        self._guest_id = guest_id

    def execute(self) -> None:
        try:
            guest = self._session.query(GuestUserModel).filter(GuestUserModel.id == self._guest_id).first()
            if not guest:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Guest not found"
                )
            self._session.delete(guest)

            responsible_guests = self._session.query(GuestUserModel).filter(GuestUserModel.g_responsible_id == self._guest_id).all()
            for responsible_guest in responsible_guests:
                self._session.delete(responsible_guest)

            self._session.commit()      
        except Exception as e:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )