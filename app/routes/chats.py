from fastapi import APIRouter, HTTPException
from app.models import ChatCreate
from app import crud

router = APIRouter()

@router.post("/")
async def store_chat(chat: ChatCreate):
    data = await crud.create_chat(
        conversation_id=chat.user_id + "_conv",
        user_id=chat.user_id,
        messages=[msg.dict() for msg in chat.messages]
    )
    return {"status": "success", "chat": data}

@router.get("/{conversation_id}")
async def retrieve_chat(conversation_id: str):
    chat = await crud.get_chat(conversation_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.delete("/{conversation_id}")
async def remove_chat(conversation_id: str):
    deleted = await crud.delete_chat(conversation_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"status": "deleted"}
