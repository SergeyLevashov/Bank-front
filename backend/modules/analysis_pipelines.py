async def run_trends_pipeline(
    bank_names: List[str],
    product_type: str,
    period: str,
) -> TrendsResponse:
    """Trends pipeline with single-bank only. Always proper summary and plot."""
    product_code = _normalize_product_type(product_type)
    time_period = _normalize_period(period)

    # ALWAYS use only 1 bank
    bank_name = bank_names[0] if bank_names else ""
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
        points.append(TrendPoint(label=label, value=value))

    raw_summary = result.get("summary")
    # Ensure summary is a list of strings, never single string or None
    if isinstance(raw_summary, str):
        summary = [raw_summary]
    elif isinstance(raw_summary, list):
        summary = [str(x) for x in raw_summary]
    else:
        summary = []

    # Generate timeline chart
    charts = {}
    try:
        fig = _chart_generator.generate_timeline_chart(timeline)
        charts["trends"] = _chart_generator.save_chart_html(fig)
    except Exception:
        pass

    return TrendsResponse(
        bank_name=bank_name,
        bank_names=[bank_name],
        product_type=product_type,
        period=period,
        generated_at=datetime.utcnow(),
        summary=summary,
        points=points,
        charts=charts if charts else None,
    )
