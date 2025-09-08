# app/routes/auth.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, UserOut
from app.db.mongo import users_collection
from app.core.security import verify_password
from app.core.jwt import create_access_token

router = APIRouter()

@router.post("/login", response_model=UserOut)
async def login(data: LoginRequest):
    user = await users_collection.find_one({"username": data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not await verify_password(data.password, user["passwordHash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({
        "id": str(user["_id"]),
        "username": user["username"],
        "userType": user["userType"]
    })

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "userType": user["userType"],
        "token": token
    }
