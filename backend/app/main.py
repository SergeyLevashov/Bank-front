from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api import urgent, trends, banks


settings = get_settings()

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
)


# CORS для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(urgent.router, prefix="/api/urgent", tags=["urgent"])
app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
app.include_router(banks.router, prefix="/api/banks", tags=["banks"])
