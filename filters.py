from typing import List
from datetime import datetime

def filter_by_date(messages: List[dict], start_iso: str, end_iso: str) -> List[dict]:
    """Filter messages whose ISO timestamps fall between start and end (inclusive)."""
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso)
    out = []
    for m in messages:
        ts = m.get("timestamp")
        if not ts:
            continue
        try:
            dt = datetime.fromisoformat(ts)
            if start <= dt <= end:
                out.append(m)
        except Exception:
            continue
    return out

def filter_by_keyword(messages: List[dict], keyword: str) -> List[dict]:
    """Filter messages containing a specific keyword (case-insensitive)."""
    kw = keyword.lower()
    return [m for m in messages if kw in (m.get("message", "").lower())]
