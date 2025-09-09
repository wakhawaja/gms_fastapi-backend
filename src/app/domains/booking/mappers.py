# app/domains/parts/mappers.py

def map_part_out(doc):
    def format_user(user):
        if not user:
            return None
        return {
            "id": user.get("id"),
            "username": user.get("username"),
            "userType": user.get("userType"),
        }

    return {
        "id": str(doc["_id"]),
        "partName": doc.get("partName"),
        "partNumber": doc.get("partNumber"),
        "createdBy": format_user(doc.get("createdBy")),
        "updatedBy": format_user(doc.get("updatedBy")),
        "createdAt": str(doc.get("createdAt")) if doc.get("createdAt") else None,
        "updatedAt": str(doc.get("updatedAt")) if doc.get("updatedAt") else None,
    }
