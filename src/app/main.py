# app/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.mongo import init_db, close_db, ping_db

# Routers
from app.domains.auth.router import router as auth_router
from app.domains.parts.router import router as parts_router
from app.domains.service.router import router as service_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("✅ MongoDB connection verified at startup.")
    except Exception as exc:
        logger.exception("❌ MongoDB ping failed at startup: %s", exc)
    yield
    try:
        close_db()
        logger.info("🛑 MongoDB client closed on shutdown.")
    except Exception as exc:
        logger.exception("⚠️ Error while closing MongoDB client: %s", exc)

app = FastAPI(
    title="Garage Management System",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api")
app.include_router(parts_router, prefix="/api")
app.include_router(service_router, prefix="/api")

# Health checks
@app.get("/api/health", tags=["Health"])
def health_check():
    return {"ok": True}

@app.get("/api/db-health", tags=["Health"])
async def db_health_check():
    ok = await ping_db()
    return {"database": "ok" if ok else "unreachable"}
