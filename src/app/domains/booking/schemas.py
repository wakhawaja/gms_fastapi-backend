from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class BookingCreate(BaseModel):
    vehicleId: str
    customerId: str
    date: datetime
    serviceType: str
    status: Literal["pending", "confirmed", "completed", "cancelled"] = "pending"

class BookingUpdate(BaseModel):
    date: Optional[datetime]
    serviceType: Optional[str]
    status: Optional[Literal["pending", "confirmed", "completed", "cancelled"]]

class BookingOut(BaseModel):
    id: str
    vehicleId: str
    customerId: str
    date: datetime
    serviceType: str
    status: str
    createdAt: datetime
    updatedAt: datetime
