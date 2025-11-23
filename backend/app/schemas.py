from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ====== Urgent Mode ======


class UrgentRequest(BaseModel):
    bank_name: str = Field(..., description="Например: Сбербанк")
    competitor_name: str = Field(..., description="Например: Райффайзенбанк")
    product_type: str = Field(..., description="Например: кредитная карта")


class ComparisonItem(BaseModel):
    parameter: str
    sber_value: str
    competitor_value: str
    comment: Optional[str] = None


class UrgentResponse(BaseModel):
    bank_name: str
    competitor_name: str
    product_type: str
    generated_at: datetime
    comparison_table: List[ComparisonItem]
    insights: List[str]
    report_url: Optional[str] = None


# ====== Trends Mode ======


class TrendsRequest(BaseModel):
    bank_name: str
    product_type: str
    period: str = Field(..., description="Например: 12m, 6m, 3m")


class TrendPoint(BaseModel):
    label: str  # например, "Янв 2025"
    value: float  # ставка/комиссия и т.п.


class TrendsResponse(BaseModel):
    bank_name: str
    product_type: str
    period: str
    generated_at: datetime
    summary: List[str]
    points: List[TrendPoint]
