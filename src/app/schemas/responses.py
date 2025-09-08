from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar("T")

class ResponseMeta(BaseModel):
    total: Optional[int] = None
    page: Optional[int] = None
    size: Optional[int] = None

class ApiResponse(BaseModel, Generic[T]):
    ok: bool = True
    data: Optional[T] = None
    meta: Optional[ResponseMeta] = None
    error: Optional[str] = None
