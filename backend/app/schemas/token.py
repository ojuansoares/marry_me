from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str 
    user_email: str
    user_id: int