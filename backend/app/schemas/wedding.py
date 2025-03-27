from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime


class WeddingCreate(BaseModel):
    w_name: str
    w_date: datetime
    w_location: str
    w_description: str
    w_status: Literal['active', 'postponed', 'cancelled']
