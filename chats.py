from fastapi import APIRouter, HTTPException
from models import ChatCreate, ChatOut
import crud

router = APIRouter()

@router.post("", response_model=str, summary="Create or append to a conversation")
async def create_chat_endpoint(payload: ChatCreate):
    conv_id = await crud.create_chat(payload)
    return conv_id

@router.get("/{conversation_id}", response_model=ChatOut)
async def get_chat_endpoint(conversation_id: str):
    chat = await crud.get_chat(conversation_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.delete("/{conversation_id}", summary="Delete a conversation")
async def delete_chat_endpoint(conversation_id: str):
    ok = await crud.delete_chat(conversation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Chat not found or already deleted")
    return {"deleted": True, "conversation_id": conversation_id}
