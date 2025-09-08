from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

# Initialize Mongo client
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Lifecycle: ping, init, close
async def ping_db() -> bool:
    try:
        await client.admin.command("ping")
        return True
    except Exception:
        return False

async def init_db() -> None:
    from app.db.indexes import ensure_indexes
    await ping_db()
    await ensure_indexes()

def close_db() -> None:
    client.close()
