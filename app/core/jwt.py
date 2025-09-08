# app/core/jwt.py
from jose import jwt
from app.config import JWT_SECRET, JWT_ALGORITHM

def create_access_token(data: dict, expires_in: int = 7 * 24 * 60 * 60) -> str:
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
