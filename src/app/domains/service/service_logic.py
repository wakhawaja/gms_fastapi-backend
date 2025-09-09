# app/domains/service/service_logic.py
from app.core.audit import build_create_doc, build_update_ops
from app.domains.service import service_db
from app.domains.service.mappers import map_service_out
from app.schemas.common import UserInDB
from fastapi import HTTPException

async def create_service_logic(data: dict, user: UserInDB):
    doc = build_create_doc(data, user.model_dump())
    try:
        service = await service_db.create_service(doc)
        return map_service_out(service)
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=400, detail="Service with this name already exists")
        raise

async def get_services_logic():
    services = await service_db.get_all_services()
    return {
        "total": len(services),
        "data": [map_service_out(s) for s in services]
    }

async def get_service_by_id_logic(service_id: str):
    service = await service_db.get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return map_service_out(service)

async def update_service_logic(service_id: str, update_data: dict, user: UserInDB):
    update_fields = build_update_ops(update_data, user.model_dump())
    updated = await service_db.update_service(service_id, update_fields)
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found")
    return map_service_out(updated)

async def delete_service_logic(service_id: str, user: UserInDB):
    deleted = await service_db.soft_delete_service(service_id, user.model_dump())
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted successfully"}
