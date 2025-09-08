from bson import ObjectId
from fastapi import HTTPException, status

def validate_object_id(id_str: str) -> ObjectId:
    """Validate and convert a string to ObjectId, or raise 400."""
    if not ObjectId.is_valid(id_str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ObjectId"
        )
    return ObjectId(id_str)

def str_object_id(oid: ObjectId) -> str:
    """Convert ObjectId to string safely."""
    return str(oid) if oid else None
