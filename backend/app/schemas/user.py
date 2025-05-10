from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal
from datetime import datetime
from app.schemas.constants import Group

# Para dados de entrada (base)
# Quando o cliente envia dados de um usuário
class UserBase(BaseModel):
    u_name: str
    u_email: EmailStr
    u_phone: str
    u_type: Literal['fiance', 'guest']

# Para dados de entrada (criação)
# Quando o cliente envia dados para criar um usuário
class UserCreate(UserBase):
    u_password: str

    @field_validator('u_type')
    def validate_u_type(cls, u_type):
        if u_type not in ['fiance', 'guest']:
            raise ValueError('Invalid user type')
        return u_type

# Para dados de atualização
# Quando o cliente envia dados para atualizar um usuário
class UserUpdate(BaseModel):
    u_name: str | None = None
    u_email: EmailStr | None = None
    u_phone: str | None = None
    u_password: str | None = None

# Para dados de saída (base)
# Quando o cliente recebe dados de um usuário, sem senha
class UserInDBBase(UserBase):
    id: int
    u_created_at: datetime

# Para dados de saída
# Quando o cliente recebe dados de um usuário
class User(UserInDBBase):
    pass

    class Config:
        from_attributes = True

# Para dados de saída (privados)
# Quando o cliente recebe dados de um usuário (sem senha)
class UserInDB(UserInDBBase):
    u_password_hash: str 

    class Config:
        from_attributes = True

class CreateWeddingGuest(BaseModel):
    g_group_id: int
    g_responsible_id: int | None = None
    g_name: str
    g_phone: str

    @field_validator('g_group_id')
    def validate_g_group_id(cls, g_group_id):
        valid_group_ids = {group["id"] for group in Group.ALL_GROUPS}
        if g_group_id not in valid_group_ids:
            raise ValueError(f"Invalid group ID. Must be one of {valid_group_ids}")
        return g_group_id

class GuestResponse(BaseModel):
    id: int
    g_wedding_id: int
    g_user_id: int | None = None
    g_group_id: int | None = None
    g_responsible_id: int | None = None
    g_name: str
    g_phone: str | None = None
    g_qr_code: str | None = None
    g_confirmed: bool | None = None
    g_created_at: datetime

    class Config:
        from_attributes = True