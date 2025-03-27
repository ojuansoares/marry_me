# -*- encoding: utf-8 -*-

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.models import User as UserModel
from app.core.security import get_password_hash


class CreateUserController:
    def __init__(self, session: Session, user: UserCreate) -> None:
        self._session = session
        self._user = user

    def execute(self) -> User:
        try:
            db_user = GetUserByEmailController.execute(self._session, u_email=self._user.u_email)
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

    def create_user(self) -> User:
        hashed_password = get_password_hash(self._user.u_password)
        db_user = UserModel(
            u_name=self._user.u_name,
            u_email=self._user.u_email,
            u_password_hash=hashed_password,
            u_phone=self._user.u_phone,
            u_type=self._user.u_type
        )
        self._session.add(db_user)
        return db_user


class GetUserController:
    @staticmethod
    def execute(session: Session, user_id: int) -> UserModel:
        db_user = session.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user

class GetUserByEmailController:
    @staticmethod
    def execute(session: Session, u_email: str) -> UserModel | None:
        return session.query(UserModel).filter(UserModel.u_email == u_email).first()

class UpdateUserController:
    @staticmethod
    def execute(session: Session, user_id: int, user: UserUpdate) -> UserModel:
        db_user = GetUserController.execute(session, user_id=user_id)
        
        update_data = user.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
            
        for field, value in update_data.items():
            setattr(db_user, f"u_{field}", value)
            
        session.commit()
        session.refresh(db_user)
        return db_user

class DeleteUserController:
    @staticmethod
    def execute(session: Session, user_id: int) -> None:
        db_user = GetUserController.execute(session, user_id=user_id)
        session.delete(db_user)
        session.commit()