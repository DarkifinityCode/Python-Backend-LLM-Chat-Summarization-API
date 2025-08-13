from fastapi import APIRouter, HTTPException
from app.models import SummarizeRequest, SummarizeResponse
from ..utils.summarizer import summarize_chat  # Changed to relative import
from app import crud

router = APIRouter()

@router.post("/")
async def summarize(request: SummarizeRequest):
    chat = await crud.get_chat(request.conversation_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    summary, keywords, sentiment = summarize_chat(chat["messages"])
    return SummarizeResponse(summary=summary, keywords=keywords, sentiment=sentiment)
