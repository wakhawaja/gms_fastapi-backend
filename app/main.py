# app/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.db.mongo import init_db, close_db, ping_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    try:
        await init_db()
        logger.info("✅ MongoDB connection verified at startup.")
    except Exception as exc:
        logger.exception("❌ MongoDB ping failed at startup: %s", exc)
        # Optionally: re-raise to prevent app from starting
        # raise

    yield

    # --- Shutdown ---
    try:
        close_db()
        logger.info("🛑 MongoDB client closed on shutdown.")
    except Exception as exc:
        logger.exception("⚠️ Error while closing MongoDB client: %s", exc)

app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

@app.get("/api/health")
def health_check():
    return {"ok": True}

@app.get("/api/db-health")
async def db_health_check():
    ok = await ping_db()
    return {"database": "ok" if ok else "unreachable"}
