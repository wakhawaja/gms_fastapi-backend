from typing import Optional, Dict, Any
from app.db.collections import users_collection

async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    return await users_collection.find_one({"username": username})
