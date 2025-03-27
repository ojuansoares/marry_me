from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

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

    class Config:
        from_attributes = True

# Para dados de saída (completo)
# Quando o cliente recebe todos os dados de um usuário
class User(UserInDBBase):
    pass

# Para dados de saída (privados)
# Quando o cliente recebe dados de um usuário (sem senha)
class UserInDB(UserInDBBase):
    u_password_hash: str 