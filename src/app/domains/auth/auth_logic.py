from fastapi import HTTPException, status
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.domains.auth.auth_db import get_user_by_username

async def login_and_issue_token(username: str, password: str):
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # verify_password is synchronous per updated core/security.py
    if not verify_password(password, user["passwordHash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({
        "id": str(user["_id"]),
        "username": user["username"],
        "userType": user["userType"],
    })

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "userType": user["userType"],
        "token": token,
    }
