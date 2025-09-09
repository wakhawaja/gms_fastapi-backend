# app/core/auth.py
from fastapi import Depends, HTTPException, status, Header
from jose import jwt, JWTError
from typing import Optional, List
from bson import ObjectId
from app.config.settings import settings
from app.db.mongo import db
from app.schemas.common import UserInDB


async def get_current_user(authorization: Optional[str] = Header(None)) -> UserInDB:
    """Extracts JWT from Authorization header, validates it, and loads user from DB."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = await db.users.find_one({"_id": ObjectId(user_id)}, {"passwordHash": 0})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    user["id"] = str(user["_id"])
    try:
        return UserInDB(**user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid user structure: {e}")


def require_role(*roles: List[str]):
    """Role guard to restrict endpoints to certain user types."""
    async def _guard(user: UserInDB = Depends(get_current_user)):
        if user.userType not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return _guard
