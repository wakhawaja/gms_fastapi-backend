from bson import ObjectId
from fastapi import HTTPException
from app.domains.parts import parts_db
from app.domains.parts.mappers import map_part_out
from app.db.collections import users_collection
from pymongo.errors import DuplicateKeyError


async def _build_users_map(*user_ids):
    """Helper to fetch and build user info map."""
    uids = [uid for uid in user_ids if uid]
    users_map = {}

    if uids:
        async for user in users_collection.find({"_id": {"$in": uids}}, {"username": 1, "userType": 1}):
            users_map[user["_id"]] = user

    return users_map


async def create_part(data: dict, user_id: str):
    try:
        created = await parts_db.insert_part(data, user_id)
    except ValueError:
        raise HTTPException(status_code=409, detail="Duplicate part entry")

    users_map = await _build_users_map(created.get("createdBy"), created.get("updatedBy"))
    return map_part_out(created, users_map)

async def update_part(id: str, data: dict, user_id: str):
    _id = ObjectId(id)
    try:
        updated = await parts_db.update_part(_id, data, user_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Duplicate part entry")
    
    if not updated:
        raise HTTPException(status_code=404, detail="Part not found")
    
    users_map = await _build_users_map([updated], users_collection)
    return map_part_out(updated, users_map)


async def delete_part(id: str):
    _id = ObjectId(id)
    deleted = await parts_db.delete_part(_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Part not found")
    return {"message": "Part deleted successfully"}
