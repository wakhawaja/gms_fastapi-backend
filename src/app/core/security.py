# app/core/security.py
import bcrypt
from typing import Union


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    Returns a hash string suitable for storing in the database.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: Union[str, bytes]) -> bool:
    """
    Check whether the plain password matches the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
