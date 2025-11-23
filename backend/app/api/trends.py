from fastapi import APIRouter

from app.schemas import TrendsRequest, TrendsResponse
from modules.analysis_pipelines import run_trends_pipeline

router = APIRouter()


@router.post("/", response_model=TrendsResponse)
async def create_trends_report(payload: TrendsRequest) -> TrendsResponse:
    """
    Trends mode with multi-bank support:
    анализ трендов по продукту для нескольких банков.
    """
    return await run_trends_pipeline(
        bank_names=payload.bank_names,
        product_type=payload.product_type,
        period=payload.period,
    )
