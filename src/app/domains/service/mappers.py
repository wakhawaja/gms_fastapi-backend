from bson import ObjectId
from app.db.collections import users_collection

async def _user_payload(user_id, users_map=None):
    if not user_id:
        return None

    if users_map and user_id in users_map:
        user = users_map.get(user_id)
    else:
        user = await users_collection.find_one({"_id": ObjectId(user_id)}, {"username": 1, "userType": 1})

    if not user:
        return {"id": str(user_id), "username": None, "userType": None}

    return {
        "id": str(user_id),
        "username": user.get("username"),
        "userType": user.get("userType")
    }

async def map_service_out(doc, users_map=None):
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "enabled": bool(doc.get("enabled", True)),
        "createdBy": await _user_payload(doc.get("createdBy"), users_map),
        "updatedBy": await _user_payload(doc.get("updatedBy"), users_map),
        "deletedBy": await _user_payload(doc.get("deletedBy"), users_map),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt"),
        "deletedAt": doc.get("deletedAt"),
        "__v": doc.get("__v", 0),
    }
