# domains/auth/router.py
from fastapi import APIRouter
from app.domains.auth.schemas import LoginRequest, UserOut
from app.domains.auth.auth_logic import login_and_issue_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=UserOut)
async def login(data: LoginRequest):
    return await login_and_issue_token(data.username, data.password)
