from pydantic import BaseModel, field_validator
from datetime import datetime
from app.schemas.constants import Group

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
    
class Invite(BaseModel):
    w_id: int
    w_date: datetime
    w_fiance_name: str
    w_bride_name: str
    w_location: str
    w_description: str
    g_id: int