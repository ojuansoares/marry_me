# -*- encoding: utf-8 -*-

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate, UserUpdate, UserInDB
from app.models.models import User as UserModel
from app.core.security import get_password_hash
from app.services.user_service import get_user_by_email



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
