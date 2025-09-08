from datetime import timedelta, datetime
from jose import jwt, JWTError
from typing import Union, Dict, Any
from app.config.settings import settings


def create_access_token(
    data: dict,
    expires_delta: Union[int, timedelta] = timedelta(days=7)
) -> str:
    """
    Create a JWT token with given payload and expiration.
    `expires_delta` can be int (seconds) or timedelta.
    """
    if isinstance(expires_delta, int):
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + expires_delta

    to_encode = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> Union[Dict[str, Any], None]:
    """
    Decode and validate a JWT. Returns payload if valid, or None if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None
