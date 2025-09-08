# app/domains/parts/mappers.py

from typing import Dict, Any, Optional
from bson import ObjectId

def map_part_out(doc: Dict[str, Any], users_map: Dict[ObjectId, Dict[str, Any]]) -> Dict[str, Any]:
    def format_user(uid: Optional[ObjectId]) -> Optional[Dict[str, Optional[str]]]:
        if not uid:
            return None

        user_data = users_map.get(uid)
        return {
            "id": str(uid),
            "username": user_data.get("username") if user_data else None,
            "userType": user_data.get("userType") if user_data else None,
        }

    return {
        "id": str(doc["_id"]),
        "partName": doc.get("partName"),
        "partNumber": doc.get("partNumber"),
        "createdBy": format_user(doc.get("createdBy")),
        "updatedBy": format_user(doc.get("updatedBy")),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt"),
        "__v": doc.get("__v", 0),
    }
