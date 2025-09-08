from typing import Optional
from pydantic import BaseModel
from typing import Literal

class AuditUser(BaseModel):
    """Minimal user info for createdBy/updatedBy/deletedBy fields."""
    id: str
    username: Optional[str]
    userType: Optional[str]

from pydantic import BaseModel
from typing import Literal

class UserInDB(BaseModel):
    id: str
    username: str
    userType: Literal["admin", "staff", "user"]  # or adjust values to match your app
