# app/core/jwt.py
from datetime import timedelta
from jose import jwt, JWTError
from typing import Union, Dict, Any

from app.config.settings import settings
from app.core.time import utcnow  # ✅ Use your custom utcnow()

def create_access_token(
    data: dict,
    expires_delta: Union[int, timedelta] = timedelta(days=7)
) -> str:
    """
    Create a JWT token with given payload and expiration.
    `expires_delta` can be an int (seconds) or a timedelta.
    """
    expire = utcnow() + (
        timedelta(seconds=expires_delta) if isinstance(expires_delta, int) else expires_delta
    )

    to_encode = {**data, "exp": expire}

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_access_token(token: str) -> Union[Dict[str, Any], None]:
    """
    Decode and validate a JWT. Returns payload if valid, or None if invalid.
    """
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        return None
