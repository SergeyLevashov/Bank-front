
from fastapi import APIRouter

from app.schemas import TrendsRequest, TrendsResponse
from modules.analysis_pipelines import run_trends_pipeline

router = APIRouter()


@router.post("/", response_model=TrendsResponse)
async def create_trends_report(payload: TrendsRequest) -> TrendsResponse:
    """
    Trends mode:
    анализ трендов по продукту/банку на основе модуля TrendsAnalyzer.
    """
    return await run_trends_pipeline(
        bank_name=payload.bank_name,
        product_type=payload.product_type,
        period=payload.period,
    )
