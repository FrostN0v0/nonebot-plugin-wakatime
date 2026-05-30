def format_count(value: int) -> str:
    return f"{value:,}"


def format_compact_count(value: int) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def format_percent(value: float) -> str:
    return f"{value:.1f}"


def ring_dasharray(percent: float) -> str:
    return f"{int(percent / 100 * 75)} 100"


TEMPLATE_FILTERS = {
    "count": format_count,
    "compact_count": format_compact_count,
    "percent": format_percent,
    "ring_dasharray": ring_dasharray,
}
