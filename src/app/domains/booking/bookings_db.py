from app.db.collections import bookings_collection
from bson import ObjectId

async def insert_booking(data):
    result = await bookings_collection.insert_one(data)
    return result.inserted_id

async def get_booking_by_id(id):
    return await bookings_collection.find_one({"_id": ObjectId(id)})

async def get_all_bookings():
    return [doc async for doc in bookings_collection.find()]

async def update_booking(id, update):
    return await bookings_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update}, return_document=True
)
