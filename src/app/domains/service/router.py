# domains/service/router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from app.schemas.common import UserInDB
from app.domains.service.schemas import ServiceCreate, ServiceUpdate, ServiceOut
from app.domains.service import service_logic, service_db
from app.domains.service.mappers import map_service_out
from app.core.auth import get_current_user, require_role
from app.db.collections import users_collection

router = APIRouter(prefix="/services", tags=["Services"])

def _oid(id_str: str) -> ObjectId:
    if not ObjectId.is_valid(id_str):
        raise HTTPException(status_code=400, detail="Invalid service ID")
    return ObjectId(id_str)

@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
async def create(data: ServiceCreate, user: UserInDB = Depends(require_role("admin"))):
    return await service_logic.create_service(data.dict(), user["id"])

@router.get("/", response_model=List[ServiceOut])
async def get_all(user: UserInDB = Depends(get_current_user)):
    services = await service_db.get_all_services()

    uids = {s.get("createdBy") for s in services} | \
           {s.get("updatedBy") for s in services} | \
           {s.get("deletedBy") for s in services}
    uids = {uid for uid in uids if uid}

    users_map = {}
    if uids:
        async for user_doc in users_collection.find({"_id": {"$in": list(uids)}}, {"username": 1, "userType": 1}):
            users_map[user_doc["_id"]] = user_doc

    return [await map_service_out(s, users_map) for s in services]

@router.patch("/{id}", response_model=ServiceOut)
async def update(id: str, data: ServiceUpdate, user: UserInDB = Depends(require_role("admin"))):
    if not data.name and data.enabled is None:
        raise HTTPException(status_code=400, detail="No fields to update")
    return await service_logic.update_service(id, data.dict(exclude_unset=True), user["id"])

@router.delete("/{id}")
async def delete(id: str, user: UserInDB = Depends(require_role("admin"))):
    return await service_logic.delete_service(id, user["id"])
