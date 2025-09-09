from app.core.audit import build_create_doc, build_update_ops
from app.domains.supplier import supplier_db
from app.domains.supplier.mappers import map_supplier_out
from app.schemas.common import UserInDB
from fastapi import HTTPException

async def create_supplier_logic(data: dict, user: UserInDB):
    doc = build_create_doc(data, user.model_dump())
    try:
        supplier = await supplier_db.create_supplier(doc)
        return map_supplier_out(supplier)
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=400, detail="Supplier with this name already exists")
        raise

async def get_suppliers_logic():
    suppliers = await supplier_db.get_all_suppliers()
    return {
        "total": len(suppliers),
        "data": [map_supplier_out(s) for s in suppliers]
    }

async def get_supplier_by_id_logic(supplier_id: str):
    supplier = await supplier_db.get_supplier_by_id(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return map_supplier_out(supplier)

async def update_supplier_logic(supplier_id: str, update_data: dict, user: UserInDB):
    update_fields = build_update_ops(update_data, user.model_dump())
    updated = await supplier_db.update_supplier(supplier_id, update_fields)
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return map_supplier_out(updated)

async def delete_supplier_logic(supplier_id: str, user: UserInDB):
    deleted = await supplier_db.soft_delete_supplier(supplier_id, user.model_dump())
    if not deleted:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"message": "Supplier deleted successfully"}
