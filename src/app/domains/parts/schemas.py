from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from app.schemas.common import AuditUser
from app.constants.parts import (
    PART_NAME_MAX_LEN,
    PART_NUMBER_MAX_LEN,
    PART_NUMBER_PATTERN,
)

class PartBase(BaseModel):
    partName: str = Field(
        ...,
        min_length=1,
        max_length=PART_NAME_MAX_LEN,
        description="Name of the part",
        example="Brake Pad"
    )
    partNumber: Optional[str] = Field(
        None,
        min_length=1,
        max_length=PART_NUMBER_MAX_LEN,
        pattern=PART_NUMBER_PATTERN,
        description="Alphanumeric part number (dot, dash, underscore allowed)",
        example="BP-2024-XL"
    )

class PartCreate(PartBase):
    pass

class PartUpdate(BaseModel):
    partName: Optional[str] = Field(
        None,
        min_length=1,
        max_length=PART_NAME_MAX_LEN,
        description="Updated part name",
        example="Disc Brake Pad"
    )
    partNumber: Optional[str] = Field(
        None,
        min_length=1,
        max_length=PART_NUMBER_MAX_LEN,
        pattern=PART_NUMBER_PATTERN,
        description="Updated part number",
        example="BP-2024-XL-R2"
    )

class PartOut(PartBase):
    id: str
    createdBy: Optional[AuditUser]
    updatedBy: Optional[AuditUser]
    createdAt: Optional[str]
    updatedAt: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class PartListResponse(BaseModel):
    total: int
    data: List[PartOut]
