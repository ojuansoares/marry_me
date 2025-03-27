# -*- encoding: utf-8 -*-

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.models import User as UserModel
from app.core.security import get_password_hash


class CreateUserController:
    def __init__(self, db: Session, user: UserCreate) -> None:
        self._db = db
        self._user = user

    def execute(self) -> None:
        try:
            db_user = GetUserByEmailController.execute(self._db, email=self._user.email)
            if db_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            self.create_user()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def create_user(self) -> None:
        hashed_password = get_password_hash(self._user.password)
        db_user = UserModel(
            u_name=self._user.name,
            u_email=self._user.email,
            u_password_hash=hashed_password,
            u_phone=self._user.phone,
            u_type=self._user.type
        )
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)


class GetUserController:
    @staticmethod
    def execute(db: Session, user_id: int) -> User:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user

class GetUserByEmailController:
    @staticmethod
    def execute(db: Session, email: str) -> Optional[User]:
        return db.query(UserModel).filter(UserModel.u_email == email).first()

class UpdateUserController:
    @staticmethod
    def execute(db: Session, user_id: int, user: UserUpdate) -> User:
        db_user = GetUserController.execute(db, user_id=user_id)
        
        update_data = user.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])
            
        for field, value in update_data.items():
            setattr(db_user, f"u_{field}", value)
            
        db.commit()
        db.refresh(db_user)
        return db_user

class DeleteUserController:
    @staticmethod
    def execute(db: Session, user_id: int) -> None:
        db_user = GetUserController.execute(db, user_id=user_id)
        db.delete(db_user)
        db.commit()