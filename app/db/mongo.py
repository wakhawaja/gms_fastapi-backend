# app/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["gms_db"]
users_collection = db.users

async def ping_db() -> bool:
    """Return True if MongoDB responds to ping, else False."""
    try:
        await client.admin.command("ping")
        return True
    except Exception:
        return False

async def init_db() -> None:
    """Verify DB connectivity at startup (raises on failure)."""
    # Raises an exception if unreachable; FastAPI will log and you’ll see it.
    await client.admin.command("ping")

def close_db() -> None:
    """Close the MongoDB client at shutdown."""
    client.close()
