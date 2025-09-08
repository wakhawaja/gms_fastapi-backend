from __future__ import annotations
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, field_validator
from app.constants.parts import (
    PART_NAME_MAX_LEN,
    PART_NUMBER_MAX_LEN,
    PART_NUMBER_PATTERN,
)

class PartCreate(BaseModel):
    partName: str = Field(..., min_length=1, max_length=PART_NAME_MAX_LEN)
    partNumber: Optional[str] = Field(default=None, max_length=PART_NUMBER_MAX_LEN)

    @field_validator("partName")
    @classmethod
    def clean_name(cls, v):
        v = (v or "").strip()
        if not v:
            raise ValueError("partName cannot be blank")
        return v

    @field_validator("partNumber")
    @classmethod
    def normalize_part_number(cls, v):
        if not v:
            return None
        v = v.strip()
        if v == "":
            return None
        import re
        if not re.fullmatch(PART_NUMBER_PATTERN, v):
            raise ValueError("Invalid characters in partNumber")
        return v

class PartUpdate(BaseModel):
    partName: Optional[str]
    partNumber: Optional[str]

    @field_validator("partName")
    @classmethod
    def validate_name(cls, v):
        if v is None:
            return None
        v = v.strip()
        if not v:
            raise ValueError("partName cannot be blank")
        return v

    @field_validator("partNumber")
    @classmethod
    def validate_number(cls, v):
        if v is None:
            return None
        v = v.strip()
        if v == "":
            return None
        import re
        if not re.fullmatch(PART_NUMBER_PATTERN, v):
            raise ValueError("Invalid characters in partNumber")
        return v

class PartOut(BaseModel):
    id: str
    partName: str
    partNumber: Optional[str] = None
    createdBy: Optional[Dict[str, Optional[str]]]
    updatedBy: Optional[Dict[str, Optional[str]]]
    createdAt: datetime
    updatedAt: datetime
    __v: int
