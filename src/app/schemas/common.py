from typing import Optional, Literal
from pydantic import BaseModel

class AuditUser(BaseModel):
    id: str
    username: Optional[str]
    userType: Optional[str]

class UserInDB(BaseModel):
    id: str
    username: str
    userType: Literal["admin", "staff", "user"]
