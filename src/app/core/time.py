# app/core/time.py
from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    Returns a timezone-aware UTC datetime.
    """
    return datetime.now(timezone.utc)
