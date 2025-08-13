from fastapi import APIRouter, HTTPException
import crud
from models import InsightsResponse
from summarizer import summarize_chat

router = APIRouter()

@router.get("/{conversation_id}", response_model=InsightsResponse)
async def conversation_insights(conversation_id: str):
    chat = await crud.get_chat(conversation_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    msgs = chat.get("messages", [])
    participants = sorted({m.get("sender_id", "unknown") for m in msgs})
    count = len(msgs)
    avg_chars = round(sum(len(m.get("message", "")) for m in msgs) / count, 2) if count else 0.0

    ts = [m.get("timestamp") for m in msgs if m.get("timestamp")]
    first_ts = min(ts) if ts else None
    last_ts  = max(ts) if ts else None

    # Reuse your summarizer to get keywords + sentiment (fast fallback if no OpenAI)
    _, keywords, sentiment = summarize_chat(msgs)

    return InsightsResponse(
        conversation_id=conversation_id,
        message_count=count,
        participant_count=len(participants),
        participants=participants,
        avg_chars_per_message=avg_chars,
        first_timestamp=first_ts,
        last_timestamp=last_ts,
        keywords=keywords,
        sentiment=sentiment,
    )
