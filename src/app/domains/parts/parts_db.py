from typing import List
from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from app.db.collections import parts_collection
from app.core.audit import build_create_doc, build_update_ops

async def insert_part(data: dict, user_id: str):
    doc = build_create_doc(data, user_id)
    try:
        res = await parts_collection.insert_one(doc)
        return await parts_collection.find_one({"_id": res.inserted_id})
    except DuplicateKeyError:
        raise ValueError("duplicate")

async def update_part(_id: ObjectId, data: dict, user_id: str):
    ops = build_update_ops(data, user_id)
    return await parts_collection.find_one_and_update(
        {"_id": _id},
        ops,
        return_document=ReturnDocument.AFTER,
    )

async def delete_part(_id: ObjectId):
    return await parts_collection.find_one_and_delete({"_id": _id})

async def get_part_by_id(_id: ObjectId):
    return await parts_collection.find_one({"_id": _id})

async def get_all_parts():
    cursor = parts_collection.find({}, sort=[("createdAt", -1)])
    return [p async for p in cursor]
