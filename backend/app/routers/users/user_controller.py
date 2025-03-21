# -*- encoding: utf-8 -*-

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.models import Usuario
from app.core.security import get_password_hash

class CreateUserController:
    @staticmethod
    def execute(db: Session, user: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            db: Database session
            user: User data to create
            
        Returns:
            Created user
            
        Raises:
            HTTPException: If email is already registered
        """
        db_user = GetUserByEmailController.execute(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(user.senha)
        db_user = Usuario(
            nome=user.nome,
            email=user.email,
            senha=hashed_password,
            telefone=user.telefone,
            tipo=user.tipo
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

class ListUsersController:
    @staticmethod
    def execute(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        List users with pagination.
        
        Args:
            db: Database session
            skip: Number of users to skip
            limit: Maximum number of users to return
            
        Returns:
            List of users
        """
        return db.query(Usuario).offset(skip).limit(limit).all()

class GetUserController:
    @staticmethod
    def execute(db: Session, user_id: int) -> User:
        """
        Get a user by ID.
        
        Args:
            db: Database session
            user_id: ID of the user to get
            
        Returns:
            User data
            
        Raises:
            HTTPException: If user is not found
        """
        db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user

class GetUserByEmailController:
    @staticmethod
    def execute(db: Session, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            db: Database session
            email: Email of the user to get
            
        Returns:
            User data or None if not found
        """
        return db.query(Usuario).filter(Usuario.email == email).first()

class UpdateUserController:
    @staticmethod
    def execute(db: Session, user_id: int, user: UserUpdate) -> User:
        """
        Update a user's information.
        
        Args:
            db: Database session
            user_id: ID of the user to update
            user: Updated user data
            
        Returns:
            Updated user
            
        Raises:
            HTTPException: If user is not found
        """
        db_user = GetUserController.execute(db, user_id=user_id)
        
        update_data = user.model_dump(exclude_unset=True)
        if "senha" in update_data:
            update_data["senha"] = get_password_hash(update_data["senha"])
            
        for field, value in update_data.items():
            setattr(db_user, field, value)
            
        db.commit()
        db.refresh(db_user)
        return db_user

class DeleteUserController:
    @staticmethod
    def execute(db: Session, user_id: int) -> None:
        """
        Delete a user.
        
        Args:
            db: Database session
            user_id: ID of the user to delete
            
        Raises:
            HTTPException: If user is not found
        """
        db_user = GetUserController.execute(db, user_id=user_id)
        db.delete(db_user)
        db.commit() 