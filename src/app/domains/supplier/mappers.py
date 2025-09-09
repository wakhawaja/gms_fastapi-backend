# app/domains/supplier/mappers.py
from app.schemas.common import AuditUser
from datetime import datetime

def map_supplier_out(doc: dict) -> dict:
    def to_str(dt):
        return dt.isoformat() if isinstance(dt, datetime) else None

    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "contact": doc["contact"],
        "bankAccount": doc["bankAccount"],
        "address": doc.get("address"),
        "email": doc.get("email"),
        "createdBy": AuditUser.model_validate(doc.get("createdBy")) if doc.get("createdBy") else None,
        "updatedBy": AuditUser.model_validate(doc.get("updatedBy")) if doc.get("updatedBy") else None,
        "createdAt": to_str(doc.get("createdAt")),
        "updatedAt": to_str(doc.get("updatedAt")),
    }
