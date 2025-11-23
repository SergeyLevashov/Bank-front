from fastapi import APIRouter

from app.schemas import UrgentRequest, UrgentResponse
from modules.analysis_pipelines import run_urgent_pipeline

router = APIRouter()


@router.post("/", response_model=UrgentResponse)
async def create_urgent_report(payload: UrgentRequest) -> UrgentResponse:
    """
    Urgent mode with multi-bank support:
    быстрый сравнительный отчёт базовый банк vs несколько конкурентов по одному продукту.
    """
    return await run_urgent_pipeline(
        bank_name=payload.bank_name,
        competitor_names=payload.competitor_names,
        product_type=payload.product_type,
    )
