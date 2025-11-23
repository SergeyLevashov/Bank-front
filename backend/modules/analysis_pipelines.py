from datetime import datetime
from typing import List

from app.schemas import UrgentResponse, ComparisonItem, TrendsResponse, TrendPoint
from modules.scraper import BankDataReader
from modules.normalizer import DataNormalizer
from modules.comparator import ProductComparator
from modules.llm_comparator import LLMComparator
from modules.trends_analyzer import TrendsAnalyzer
from modules.chart_generator import ChartGenerator

# --- Helper mappings -------------------------------------------------------

PRODUCT_TYPE_MAP = {
    "кредитная карта": "credit_card",
    "кредитные карты": "credit_card",
    "credit card": "credit_card",
    "дебетовая карта": "debit_card",
    "дебетовые карты": "debit_card",
    "debit card": "debit_card",
    "вклад": "deposit",
    "вклады": "deposit",
    "deposit": "deposit",
    "потребительский кредит": "consumer_loan",
    "потребкредит": "consumer_loan",
    "consumer loan": "consumer_loan",
}


def _normalize_product_type(label: str) -> str:
    if not label:
        return "credit_card"
    key = label.strip().lower()
    return PRODUCT_TYPE_MAP.get(key, "credit_card")


BANK_NAME_MAP = {
    "сбер": "Сбер",
    "сбербанк": "Сбер",
    "sber": "Сбер",
    "sberbank": "Сбер",
    "vtb": "ВТБ",
    "втб": "ВТБ",
    "альфа": "Альфа",
    "альфа-банк": "Альфа",
    "alfa": "Альфа",
    "tinkoff": "Тинькофф",
    "тинькофф": "Тинькофф",
}


def _normalize_bank_name(label: str) -> str:
    if not label:
        return "Сбер"
    key = label.strip().lower()
    return BANK_NAME_MAP.get(key, label.strip())


MONTH_LABELS_RU = [
    "янв", "фев", "мар", "апр", "май", "июн",
    "июл", "авг", "сен", "окт", "ноя", "дек",
]


def _format_date_label(date_str: str) -> str:
    """Convert YYYY-MM-DD -> 'Май 2025' style label."""
    try:
        dt = datetime.fromisoformat(date_str)
    except Exception:
        return date_str
    month = MONTH_LABELS_RU[dt.month - 1].capitalize()
    return f"{month} {dt.year}"


PERIOD_MAP = {
    "3m": "last_3_months",
    "6m": "last_6_months",
    "12m": "last_year",
}


def _normalize_period(period: str) -> str:
    return PERIOD_MAP.get(period, "last_6_months")


# --- Singletons ------------------------------------------------------------

_scraper = BankDataReader()
_normalizer = DataNormalizer()
_comparator = ProductComparator()
_llm_comparator = LLMComparator()
_trends_analyzer = TrendsAnalyzer()
_chart_generator = ChartGenerator()


# --- Urgent pipeline -------------------------------------------------------


async def run_urgent_pipeline(
    bank_name: str,
    competitor_names: List[str],
    product_type: str,
) -> UrgentResponse:
    """Real urgent pipeline with multi-bank support.

    bank_name        – базовый банк (обычно Сбербанк)
    competitor_names – список конкурентов
    product_type     – человекочитаемый тип продукта
    """

    base_bank_internal = _normalize_bank_name(bank_name)
    product_code = _normalize_product_type(product_type)

    # Load base bank data
    sber_raw = _scraper.get_product_data(base_bank_internal, product_code)

    def _extract_first_card(raw: dict) -> dict:
        if not raw:
            return {}
        cards = raw.get("карты")
        if isinstance(cards, list) and cards:
            return cards[0]
        if product_code in raw:
            cards = raw[product_code].get("карты")
            if isinstance(cards, list) and cards:
                return cards[0]
        return {}

    sber_card = _extract_first_card(sber_raw)

    # Process all competitors
    all_comparison_items: List[ComparisonItem] = []
    all_insights: List[str] = []
    comparison_raw = None  # Store last comparison for chart generation
    
    for competitor_name in competitor_names:
        competitor_internal = _normalize_bank_name(competitor_name)
        competitor_raw = _scraper.get_product_data(competitor_internal, product_code)
        competitor_card = _extract_first_card(competitor_raw)

        # Prefer LLM comparator when available
        use_llm = getattr(_llm_comparator, "is_enabled", lambda: False)()
        if use_llm:
            comparison_raw = _llm_comparator.compare_products(
                sber_card,
                competitor_card,
                product_code,
                competitor_name=competitor_internal,
            )
        else:
            normalize_func_map = {
                "credit_card": _normalizer.normalize_credit_card,
                "debit_card": _normalizer.normalize_debit_card,
                "deposit": _normalizer.normalize_deposit,
                "consumer_loan": _normalizer.normalize_consumer_loan,
            }
            normalizer_fn = normalize_func_map.get(product_code)
            if normalizer_fn is None:
                raise ValueError(f"Unsupported product type: {product_code}")

            sber_norm = normalizer_fn(sber_card, base_bank_internal)
            competitor_norm = normalizer_fn(competitor_card, competitor_internal)

            comparison_raw = _comparator.compare_products(
                sber_norm,
                competitor_norm,
                product_code,
            )

        df = comparison_raw.get("comparison_table")
        if hasattr(df, "to_dict"):
            rows = df.to_dict(orient="records")
        else:
            rows = []

        for row in rows:
            parameter = str(row.get("Параметр", ""))
            sber_value = str(row.get("Сбер", ""))
            competitor_value = str(row.get("Конкурент", ""))
            
            # If multiple competitors, prefix parameter name
            if len(competitor_names) > 1:
                parameter = f"[{competitor_name}] {parameter}"
            
            all_comparison_items.append(
                ComparisonItem(
                    parameter=parameter,
                    sber_value=sber_value,
                    competitor_value=competitor_value,
                )
            )

        insights = comparison_raw.get("insights") or []
        recommendation = comparison_raw.get("recommendation")
        if recommendation:
            insights = list(insights) + [recommendation]
        
        # Prefix insights with bank name if multiple competitors
        if len(competitor_names) > 1:
            all_insights.extend([f"{competitor_name}: {i}" for i in insights])
        else:
            all_insights.extend(insights)

    # Generate comparison chart
    charts = {}
    try:
        if comparison_raw and len(competitor_names) > 0:
            comparison_data = {
                "comparison_table": comparison_raw.get("comparison_table")
            }
            fig = _chart_generator.generate_comparison_chart(comparison_data)
            charts["comparison"] = _chart_generator.save_chart_html(fig)
    except Exception as e:
        pass  # Charts are optional

    return UrgentResponse(
        bank_name=bank_name,
        competitor_name=competitor_names[0] if competitor_names else None,  # For backward compatibility
        competitor_names=competitor_names,
        product_type=product_type,
        generated_at=datetime.utcnow(),
        comparison_table=all_comparison_items,
        insights=all_insights,
        report_url=None,
        charts=charts if charts else None,
    )


# --- Trends pipeline -------------------------------------------------------


async def run_trends_pipeline(
    bank_names: List[str],
    product_type: str,
    period: str,
) -> TrendsResponse:
    """Trends pipeline with multi-bank support.

    Returns normalized points ready for frontend mini-chart.
    """

    product_code = _normalize_product_type(product_type)
    time_period = _normalize_period(period)

    all_points: List[TrendPoint] = []
    all_summary: List[str] = []
    
    banks_data = []
    
    for bank_name in bank_names:
        bank_internal = _normalize_bank_name(bank_name)

        result = _trends_analyzer.analyze_trends(
            bank=bank_internal,
            product_type=product_code,
            time_period=time_period,
            use_real_search=False,
        )

        timeline = result.get("timeline") or []
        points: List[TrendPoint] = []
        for item in timeline:
            date_str = item.get("date")
            rate = item.get("rate")
            if date_str is None or rate is None:
                continue
            try:
                value = float(rate)
            except (TypeError, ValueError):
                continue
            label = _format_date_label(str(date_str))
            
            # If multiple banks, add bank name to label
            if len(bank_names) > 1:
                points.append(TrendPoint(label=f"{label} ({bank_name})", value=value))
            else:
                points.append(TrendPoint(label=label, value=value))

        all_points.extend(points)

        summary = result.get("summary") or []
        if len(bank_names) > 1:
            all_summary.extend([f"{bank_name}: {s}" for s in summary])
        else:
            all_summary.extend(summary)
        
        banks_data.append({
            "bank": bank_name,
            "timeline": timeline
        })

    # Generate trends chart
    charts = {}
    try:
        if len(banks_data) > 1:
            fig = _chart_generator.generate_multiple_banks_comparison(banks_data)
            charts["trends"] = _chart_generator.save_chart_html(fig)
        elif len(banks_data) == 1:
            timeline = banks_data[0]["timeline"]
            fig = _chart_generator.generate_timeline_chart(timeline)
            charts["trends"] = _chart_generator.save_chart_html(fig)
    except Exception as e:
        pass  # Charts are optional

    return TrendsResponse(
        bank_name=bank_names[0] if bank_names else None,  # For backward compatibility
        bank_names=bank_names,
        product_type=product_type,
        period=period,
        generated_at=datetime.utcnow(),
        summary=all_summary,
        points=all_points,
        charts=charts if charts else None,
    )
