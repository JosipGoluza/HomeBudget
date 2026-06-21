from datetime import datetime, timezone, timedelta


def resolve_period(period: str) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)

    if period == "week":
        date_from = now - timedelta(days=7)
    elif period == "month":
        date_from = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "quarter":
        quarter_start_month = ((now.month - 1) // 3) * 3 + 1
        date_from = now.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "year":
        date_from = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        raise ValueError(f"Unknown period: {period}")

    return date_from, now
