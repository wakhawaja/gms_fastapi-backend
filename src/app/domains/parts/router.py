# app/domains/parts/router.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId

from app.core.auth import get_current_user, require_role
from app.domains.parts.schemas import PartCreate, PartUpdate, PartOut
from app.domains.parts import parts_db, parts_logic
from app.domains.parts.mappers import map_part_out
from app.db.collections import users_collection

router = APIRouter(prefix="/parts", tags=["Parts"])

def _oid(id_str: str) -> ObjectId:
    if not ObjectId.is_valid(id_str):
        raise HTTPException(status_code=400, detail="Invalid part ID")
    return ObjectId(id_str)


@router.post("/", response_model=PartOut, status_code=status.HTTP_201_CREATED)
async def create(data: PartCreate, user=Depends(require_role("admin"))):
    return await parts_logic.create_part(data.dict(), user["id"])


@router.get("/", response_model=List[PartOut])
async def get_all(user=Depends(get_current_user)):
    parts = await parts_db.get_all_parts()

    # Collect all user IDs (createdBy & updatedBy)
    uids = {p.get("createdBy") for p in parts} | {p.get("updatedBy") for p in parts}
    uids = {uid for uid in uids if uid}

    users_map = {}
    if uids:
        async for u in users_collection.find({"_id": {"$in": list(uids)}}, {"username": 1, "userType": 1}):
            users_map[u["_id"]] = u

    return [map_part_out(p, users_map) for p in parts]


@router.get("/{id}", response_model=PartOut)
async def get_by_id(id: str, user=Depends(get_current_user)):
    part = await parts_db.get_part_by_id(_oid(id))
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")

    # Get user info on demand
    uid_fields = [part.get("createdBy"), part.get("updatedBy")]
    uids = [uid for uid in uid_fields if uid]
    users_map = {}
    if uids:
        async for u in users_collection.find({"_id": {"$in": uids}}, {"username": 1, "userType": 1}):
            users_map[u["_id"]] = u

    return map_part_out(part, users_map)


@router.put("/{id}", response_model=PartOut)
async def update(id: str, data: PartUpdate, user=Depends(get_current_user)):
    if not data.partName and not data.partNumber:
        raise HTTPException(status_code=400, detail="No fields to update")
    return await parts_logic.update_part(id, data.dict(exclude_unset=True), user["id"])

# Not used
@router.delete("/{id}")
async def delete(id: str, user=Depends(require_role("admin"))):
    return await parts_logic.delete_part(id)
