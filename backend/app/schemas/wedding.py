from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime


class WeddingCreate(BaseModel):
    w_date: datetime
    w_location: str
    w_description: str
    w_status: Literal['active', 'postponed', 'cancelled']

class Wedding(BaseModel):
    id: int
    w_fiance_id: int
    w_date: datetime
    w_location: str
    w_description: str
    w_status: Literal['active', 'postponed', 'cancelled']
    w_created_at: datetime

    class Config:
        from_attributes = True

class WeddingUpdate(BaseModel):
    w_date: datetime | None = None
    w_location: str | None = None
    w_description: str | None = None
    w_status: Literal['active', 'postponed', 'cancelled'] | None = None

