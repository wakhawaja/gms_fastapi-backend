from fastapi import APIRouter, Depends, HTTPException
from app.domains.booking import booking_logic
from app.schemas.common import UserInDB
from app.domains.booking.schemas import BookingCreate, BookingUpdate, BookingOut
from app.core.auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingOut)
async def create(data: BookingCreate, user: UserInDB = Depends(get_current_user)):
    return await booking_logic.create_booking(data.dict(), user)

@router.get("/", response_model=list[BookingOut])
async def get_all(user: UserInDB = Depends(get_current_user)):
    return await booking_logic.get_all_bookings()

@router.get("/{id}", response_model=BookingOut)
async def get_by_id(id: str, user: UserInDB = Depends(get_current_user)):
    return await booking_logic.get_booking_by_id(id)

@router.patch("/{id}", response_model=BookingOut)
async def update(id: str, data: BookingUpdate, user: UserInDB = Depends(get_current_user)):
    return await booking_logic.update_booking(id, data.dict(exclude_unset=True), user)
