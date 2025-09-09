from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from app.domains.parts import parts_db
from app.domains.parts.mappers import map_part_out
from app.schemas.common import UserInDB
from app.core.audit import build_create_doc, build_update_ops
from app.utils.object_id import validate_object_id

async def create_part_logic(data: dict, user: UserInDB):
    audit_doc = build_create_doc(data, user.model_dump())
    try:
        part = await parts_db.create_part(audit_doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Part with this name and number already exists"
        )
    return map_part_out(part)

async def update_part_logic(part_id: str, update_data: dict, user: UserInDB):
    _id = validate_object_id(part_id)
    audit_ops = build_update_ops(update_data, user.model_dump())
    try:
        updated = await parts_db.update_part(_id, audit_ops)
        if not updated:
            raise HTTPException(status_code=404, detail="Part not found")
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Part with this name and number already exists"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return map_part_out(updated)

async def get_part_by_id_logic(part_id: str):
    _id = validate_object_id(part_id)
    part = await parts_db.get_part_by_id(_id)
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return map_part_out(part)

async def get_all_parts_logic():
    parts = await parts_db.get_all_parts()
    return {
        "total": len(parts),
        "data": [map_part_out(p) for p in parts]
    }
