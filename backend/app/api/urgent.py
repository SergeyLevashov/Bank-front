
from fastapi import APIRouter

from app.schemas import UrgentRequest, UrgentResponse
from modules.analysis_pipelines import run_urgent_pipeline

router = APIRouter()


@router.post("/", response_model=UrgentResponse)
async def create_urgent_report(payload: UrgentRequest) -> UrgentResponse:
    """
    Urgent mode:
    быстрый сравнительный отчёт базовый банк vs конкурент по одному продукту,
    использующий реальные данные из конфигов и модулей анализа.
    """
    return await run_urgent_pipeline(
        bank_name=payload.bank_name,
        competitor_name=payload.competitor_name,
        product_type=payload.product_type,
    )
