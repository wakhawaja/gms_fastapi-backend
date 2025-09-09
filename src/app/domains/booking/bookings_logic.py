from fastapi import HTTPException
from app.domains.booking import booking_db
from app.utils.audit import build_create_doc, build_update_ops
from app.schemas.common import UserInDB
from app.domains.booking.mappers import map_booking_out
from bson import ObjectId

async def create_booking(data: dict, user: UserInDB):
    audit_doc = build_create_doc(data, user.model_dump())
    _id = await booking_db.insert_booking(audit_doc)
    booking = await booking_db.get_booking_by_id(_id)
    return map_booking_out(booking)

async def get_all_bookings():
    bookings = await booking_db.get_all_bookings()
    return [map_booking_out(b) for b in bookings]

async def get_booking_by_id(id: str):
    booking = await booking_db.get_booking_by_id(ObjectId(id))
    if not booking:
        raise HTTPException(404, detail="Booking not found")
    return map_booking_out(booking)

async def update_booking(id: str, data: dict, user: UserInDB):
    audit = build_update_ops(data, user.model_dump())
    updated = await booking_db.update_booking(id, audit)
    if not updated:
        raise HTTPException(404, detail="Booking not found")
    return map_booking_out(updated)
