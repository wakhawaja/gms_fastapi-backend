from typing import Optional, List
from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from app.db.collections import services_collection
from app.core.audit import build_create_doc, build_update_ops

async def create_service_doc(data: dict, user_id: str):
    doc = build_create_doc(data, user_id=user_id)
    try:
        res = await services_collection.insert_one(doc)
        return await services_collection.find_one({"_id": res.inserted_id})
    except DuplicateKeyError:
        raise ValueError("duplicate")

async def update_service_doc(_id: ObjectId, data: dict, user_id: str):
    ops = build_update_ops(data, user_id=user_id)
    return await services_collection.find_one_and_update(
        {"_id": _id},
        ops,
        return_document=ReturnDocument.AFTER,
    )

async def soft_delete_service_doc(_id: ObjectId, user_id: str):
    from app.core.time import utcnow
    ops = build_update_ops({
        "enabled": False,
        "deletedAt": utcnow(),
        "deletedBy": ObjectId(user_id)
    }, user_id=user_id)

    return await services_collection.find_one_and_update(
        {"_id": _id, "enabled": {"$ne": False}},
        ops,
        return_document=ReturnDocument.AFTER,
    )

async def get_all_services() -> List[dict]:
    cursor = services_collection.find({}, sort=[("createdAt", -1)])
    return [s async for s in cursor]
