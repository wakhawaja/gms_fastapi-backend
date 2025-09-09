# app/domains/supplier/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.schemas.common import AuditUser


class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1)
    contact: str = Field(..., min_length=1)
    bankAccount: str = Field(..., min_length=1)
    address: Optional[str] = None
    email: Optional[EmailStr] = None


class SupplierOut(SupplierBase):
    id: str
    createdBy: Optional[AuditUser]
    updatedBy: Optional[AuditUser]
    createdAt: Optional[str]
    updatedAt: Optional[str]

    class Config:
        orm_mode = True


class SupplierListResponse(BaseModel):
    total: int
    data: List[SupplierOut]


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    bankAccount: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
