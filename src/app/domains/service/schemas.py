from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.schemas.common import AuditUser
from app.constants.service import (SERVICE_NAME_MIN,SERVICE_NAME_MAX)

class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=SERVICE_NAME_MIN, max_length=SERVICE_NAME_MAX)
    enabled: Optional[bool] = True

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("Service name is required")
        return v

class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=SERVICE_NAME_MAX)
    enabled: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def strip_if_present(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            raise ValueError("Service name cannot be blank")
        return v

class ServiceOut(BaseModel):
    id: str
    name: str
    enabled: bool
    createdBy: Optional[AuditUser]
    updatedBy: Optional[AuditUser]
    deletedBy: Optional[AuditUser] = None
    createdAt: datetime
    updatedAt: datetime
    deletedAt: Optional[datetime] = None
    __v: int
