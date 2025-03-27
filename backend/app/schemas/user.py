from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

class UserBase(BaseModel):
    u_name: str
    u_email: EmailStr
    u_phone: str
    u_type: Literal['fiance', 'guest']

class UserCreate(UserBase):
    u_password: str

class UserUpdate(BaseModel):
    u_name: str | None = None
    u_email: EmailStr | None = None
    u_phone: str | None = None
    u_password: str | None = None

class UserInDBBase(UserBase):
    id: int
    u_created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    u_password_hash: str 