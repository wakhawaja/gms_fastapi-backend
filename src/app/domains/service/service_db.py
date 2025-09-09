# app/domains/service/service_db.py
from app.db.collections import services_collection
from pymongo import ReturnDocument
from bson import ObjectId

async def create_service(doc: dict):
    result = await services_collection.insert_one(doc)
    return await services_collection.find_one({"_id": result.inserted_id})

async def get_all_services():
    cursor = services_collection.find({"isDeleted": {"$ne": True}}).sort("createdAt", -1)
    return await cursor.to_list(length=None)

async def get_service_by_id(service_id: str):
    return await services_collection.find_one({
        "_id": ObjectId(service_id),
        "isDeleted": {"$ne": True}
    })

async def update_service(service_id: str, update_fields: dict):
    return await services_collection.find_one_and_update(
        {
            "_id": ObjectId(service_id),
            "isDeleted": {"$ne": True}
        },
        update_fields,
        return_document=ReturnDocument.AFTER
    )

async def soft_delete_service(service_id: str, deleted_by: dict):
    return await services_collection.find_one_and_update(
        {
            "_id": ObjectId(service_id),
            "isDeleted": {"$ne": True}
        },
        {"$set": {"isDeleted": True, "deletedBy": deleted_by}},
        return_document=ReturnDocument.AFTER
    )
