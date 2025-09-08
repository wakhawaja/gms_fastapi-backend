# app/schemas/auth.py
from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: str
    username: str
    userType: str
    token: str
