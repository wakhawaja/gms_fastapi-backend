from app.db.collections import parts_collection
from pymongo import ReturnDocument
from bson import ObjectId
from typing import Dict, Any

async def create_part(doc: Dict[str, Any]):
    result = await parts_collection.insert_one(doc)
    return await parts_collection.find_one({"_id": result.inserted_id})

async def get_all_parts():
    cursor = parts_collection.find({}).sort("createdAt", -1)
    return await cursor.to_list(length=None)

async def get_part_by_id(part_id: ObjectId):
    return await parts_collection.find_one({"_id": part_id})

async def update_part(part_id: ObjectId, update_fields: Dict[str, Any]):
    return await parts_collection.find_one_and_update(
        {"_id": part_id},
        update_fields,
        return_document=ReturnDocument.AFTER
    )
