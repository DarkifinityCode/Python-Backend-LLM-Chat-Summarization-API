from fastapi import APIRouter, HTTPException
from models import SummarizeRequest, SummarizeResponse
import crud
from summarizer import summarize_chat

router = APIRouter()

@router.post("", response_model=SummarizeResponse)
async def summarize_endpoint(payload: SummarizeRequest):
    chat = await crud.get_chat(payload.conversation_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    summary, keywords, sentiment = summarize_chat(chat["messages"])
    return SummarizeResponse(summary=summary, keywords=keywords, sentiment=sentiment)
