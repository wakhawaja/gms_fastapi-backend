# app/domains/supplier/supplier_db.py
from app.db.collections import suppliers_collection
from pymongo import ReturnDocument
from bson import ObjectId

async def create_supplier(doc: dict):
    result = await suppliers_collection.insert_one(doc)
    return await suppliers_collection.find_one({"_id": result.inserted_id})

async def get_all_suppliers():
    cursor = suppliers_collection.find({"isDeleted": {"$ne": True}}).sort("createdAt", -1)
    return await cursor.to_list(length=None)

async def get_supplier_by_id(supplier_id: str):
    return await suppliers_collection.find_one({
        "_id": ObjectId(supplier_id),
        "isDeleted": {"$ne": True}
    })

async def update_supplier(supplier_id: str, update_fields: dict):
    return await suppliers_collection.find_one_and_update(
        {
            "_id": ObjectId(supplier_id),
            "isDeleted": {"$ne": True}  # Prevent update on deleted supplier
        },
        update_fields,
        return_document=ReturnDocument.AFTER
    )

async def soft_delete_supplier(supplier_id: str, deleted_by: dict):
    return await suppliers_collection.find_one_and_update(
        {
            "_id": ObjectId(supplier_id),
            "isDeleted": {"$ne": True}  # Prevent re-deleting
        },
        {"$set": {"isDeleted": True, "deletedBy": deleted_by}},
        return_document=ReturnDocument.AFTER
    )