from typing import List
from datetime import datetime

def filter_by_date(messages: List[dict], start_date: datetime, end_date: datetime) -> List[dict]:
    """Filter messages between two dates."""
    return [
        msg for msg in messages
        if start_date <= datetime.fromisoformat(msg["timestamp"]) <= end_date
    ]

def filter_by_keyword(messages: List[dict], keyword: str) -> List[dict]:
    """Filter messages containing a specific keyword."""
    return [
        msg for msg in messages
        if keyword.lower() in msg["message"].lower()
    ]
