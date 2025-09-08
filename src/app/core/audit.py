from typing import Dict, Any
from bson import ObjectId
from app.core.time import utcnow


def build_create_doc(base: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Builds a document with audit fields for creation:
    - Sets createdAt, createdBy, updatedAt, updatedBy
    - Starts __v at 0
    """
    now = utcnow()
    oid = ObjectId(user_id)
    return {
        **base,
        "createdAt": now,
        "createdBy": oid,
        "updatedAt": now,
        "updatedBy": oid,
        "__v": 0,
    }


def build_update_ops(set_fields: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Builds MongoDB update operators for an update:
    - $set: includes updatedAt, updatedBy, plus any custom fields
    - $inc: increments __v by 1
    """
    now = utcnow()
    oid = ObjectId(user_id)

    return {
        "$set": {
            **set_fields,
            "updatedAt": now,
            "updatedBy": oid,
        },
        "$inc": {"__v": 1},
    }
