from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App info
    PROJECT_NAME: str = "GMS Backend"
    API_PREFIX: str = "/api"

    # Database
    MONGO_URI: str = Field(..., env="MONGO_URI")
    MONGO_DB_NAME: str = "gms_db"

    # Auth / JWT
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # pydantic-settings v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,   # "PORT" becomes "port"
        extra="ignore",         # <-- THIS fixes the error
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
