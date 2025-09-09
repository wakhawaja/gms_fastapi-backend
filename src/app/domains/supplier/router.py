# app/domains/supplier/router.py
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user, require_role
from app.schemas.common import UserInDB
from app.domains.supplier import supplier_logic
from app.domains.supplier.schemas import SupplierCreate, SupplierUpdate, SupplierOut,SupplierListResponse
from typing import List, Dict, Any

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.post("/", response_model=SupplierOut)
async def create_supplier(
    data: SupplierCreate,
    user: UserInDB = Depends(require_role("admin", "staff"))
):
    return await supplier_logic.create_supplier_logic(data.dict(), user)

@router.get("/", response_model=SupplierListResponse)
async def get_suppliers(user: UserInDB = Depends(get_current_user)):
    return await supplier_logic.get_suppliers_logic()

@router.get("/{supplier_id}", response_model=SupplierOut)
async def get_supplier(supplier_id: str, user: UserInDB = Depends(get_current_user)):
    return await supplier_logic.get_supplier_by_id_logic(supplier_id)

@router.patch("/{supplier_id}", response_model=SupplierOut)
async def update_supplier(
    supplier_id: str,
    update_data: SupplierUpdate,
    user: UserInDB = Depends(require_role("admin", "staff"))
):
    return await supplier_logic.update_supplier_logic(supplier_id, update_data.dict(exclude_unset=True), user)

@router.delete("/{supplier_id}")
async def delete_supplier(
    supplier_id: str,
    user: UserInDB = Depends(require_role("admin"))
):
    return await supplier_logic.delete_supplier_logic(supplier_id, user)
