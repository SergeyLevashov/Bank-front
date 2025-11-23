from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
    api_title: str = "Bank Product Analyzer API"
    api_version: str = "0.1.0"
    backend_cors_origins: list[str] = [
        "http://localhost:5173",  # Vite dev
        "http://127.0.0.1:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    # на будущее можно добавить чтение .env
    return Settings(
        backend_cors_origins=os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
    )
