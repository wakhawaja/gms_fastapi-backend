from bson import ObjectId
from fastapi import HTTPException
from app.domains.service import service_db
from app.domains.service.mappers import map_service_out

async def create_service(data: dict, user_id: str):
    try:
        created = await service_db.create_service_doc(data, user_id)
    except ValueError:
        raise HTTPException(status_code=409, detail="Service already exists")
    return await map_service_out(created)

async def update_service(id: str, data: dict, user_id: str):
    _id = ObjectId(id)
    updated = await service_db.update_service_doc(_id, data, user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found")
    return await map_service_out(updated)

async def delete_service(id: str, user_id: str):
    _id = ObjectId(id)
    deleted = await service_db.soft_delete_service_doc(_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Already deleted or not found")
    return {"message": "Service disabled (soft-deleted)"}
