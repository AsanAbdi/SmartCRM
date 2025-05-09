from datetime import datetime, timezone, date


def utcnow_time() -> datetime:
    return datetime.now(timezone.utc)

def utcnow_date() -> date:
    return datetime.now(timezone.utc).date()