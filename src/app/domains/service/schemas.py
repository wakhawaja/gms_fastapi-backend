from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.common import AuditUser

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=1)
    enabled: Optional[bool] = True  # Optional with default

class ServiceCreate(ServiceBase):
    """Schema for creating a new service."""
    pass

class ServiceUpdate(BaseModel):
    """Schema for updating an existing service."""
    name: Optional[str] = Field(None, min_length=1)
    enabled: Optional[bool] = None

class ServiceOut(ServiceBase):
    """Schema for service output with audit fields."""
    id: str
    createdBy: Optional[AuditUser]
    updatedBy: Optional[AuditUser]
    createdAt: Optional[str]
    updatedAt: Optional[str]

    class Config:
        orm_mode = True

class ServiceListResponse(BaseModel):
    """Paginated list response for services."""
    total: int
    data: List[ServiceOut]
