from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ====== Urgent Mode ======


class UrgentRequest(BaseModel):
    bank_name: str = Field(..., description="Например: Сбербанк")
    competitor_names: List[str] = Field(..., description="Список конкурентов для сравнения")
    product_type: str = Field(..., description="Например: кредитная карта")


class ComparisonItem(BaseModel):
    parameter: str
    sber_value: str
    competitor_value: str
    comment: Optional[str] = None


class UrgentResponse(BaseModel):
    bank_name: str
    competitor_names: List[str]  # Changed to list
    product_type: str
    generated_at: datetime
    comparison_table: List[ComparisonItem]
    insights: List[str]
    report_url: Optional[str] = None
    charts: Optional[Dict[str, str]] = None  # Chart HTML strings keyed by chart name


# ====== Trends Mode ======


class TrendsRequest(BaseModel):
    bank_names: List[str] = Field(..., description="Список банков для анализа трендов")
    product_type: str
    period: str = Field(..., description="Например: 12m, 6m, 3m")


class TrendPoint(BaseModel):
    label: str  # например, "Янв 2025"
    value: float  # ставка/комиссия и т.п.


class TrendsResponse(BaseModel):
    bank_names: List[str]  # Changed to list
    product_type: str
    period: str
    generated_at: datetime
    summary: List[str]
    points: List[TrendPoint]
    charts: Optional[Dict[str, str]] = None  # Chart HTML strings keyed by chart name
