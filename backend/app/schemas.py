from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, model_validator


# ====== Urgent Mode ======


class UrgentRequest(BaseModel):
    bank_name: str = Field(..., description="Например: Сбербанк")
    # Support BOTH old and new format for backward compatibility
    competitor_name: Optional[str] = Field(None, description="Один конкурент (старый формат)")
    competitor_names: Optional[List[str]] = Field(default=None, description="Список конкурентов (новый формат)")
    product_type: str = Field(..., description="Например: кредитная карта")

    @model_validator(mode='after')
    def normalize_competitors(self):
        """Convert competitor_name to competitor_names if needed"""
        if self.competitor_names is None or len(self.competitor_names) == 0:
            if self.competitor_name:
                self.competitor_names = [self.competitor_name]
            else:
                self.competitor_names = []
        return self


class ComparisonItem(BaseModel):
    parameter: str
    sber_value: str
    competitor_value: str
    comment: Optional[str] = None


class UrgentResponse(BaseModel):
    bank_name: str
    competitor_name: Optional[str] = None  # For old clients
    competitor_names: List[str]
    product_type: str
    generated_at: datetime
    comparison_table: List[ComparisonItem]
    insights: List[str]
    report_url: Optional[str] = None
    charts: Optional[Dict[str, str]] = None


# ====== Trends Mode ======


class TrendsRequest(BaseModel):
    # Support BOTH old and new format for backward compatibility
    bank_name: Optional[str] = Field(None, description="Один банк (старый формат)")
    bank_names: Optional[List[str]] = Field(default=None, description="Список банков (новый формат)")
    product_type: str
    period: str = Field(..., description="Например: 12m, 6m, 3m")

    @model_validator(mode='after')
    def normalize_banks(self):
        """Convert bank_name to bank_names if needed"""
        if self.bank_names is None or len(self.bank_names) == 0:
            if self.bank_name:
                self.bank_names = [self.bank_name]
            else:
                self.bank_names = []
        return self


class TrendPoint(BaseModel):
    label: str  # например, "Янв 2025"
    value: float  # ставка/комиссия и т.п.


class TrendsResponse(BaseModel):
    bank_name: Optional[str] = None  # For old clients
    bank_names: List[str]
    product_type: str
    period: str
    generated_at: datetime
    summary: List[str]
    points: List[TrendPoint]
    charts: Optional[Dict[str, str]] = None
