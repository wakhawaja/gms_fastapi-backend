# app/core/auth.py
from fastapi import Depends, HTTPException, status, Header
from jose import jwt, JWTError
from typing import Optional, List
from app.config.settings import settings
from app.db.mongo import db
from bson import ObjectId

async def get_current_user(authorization: Optional[str] = Header(None)):
    """Extracts JWT from Authorization header and loads the user from DB."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = await db.users.find_one({"_id": ObjectId(user_id)}, {"passwordHash": 0})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Make id string for response/usage convenience
    user["id"] = str(user["_id"])
    return user

def require_role(*roles: List[str]):
    """Role guard; use with Depends(require_role('admin')) along with get_current_user."""
    async def _guard(user = Depends(get_current_user)):
        user_type = user.get("userType")
        if user_type not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return _guard
