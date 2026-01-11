from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Tiling System API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./tiling_system.db"
    SECRET_KEY: str = "your-secret-key-change-in-production-please-use-strong-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
