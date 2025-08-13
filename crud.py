from typing import Optional, List, Tuple
from database import db
from models import ChatCreate, Message

def _conv_id(user_id: str, conversation_id: str | None) -> str:
    return conversation_id or f"{user_id}_conv"

async def create_chat(chat: ChatCreate) -> str:
    conversation_id = _conv_id(chat.user_id, chat.conversation_id)
    doc_msgs = [m.dict() for m in chat.messages]
    await db.chats.update_one(
        {"conversation_id": conversation_id},
        {"$setOnInsert": {"user_id": chat.user_id, "conversation_id": conversation_id},
         "$push": {"messages": {"$each": doc_msgs}}},
        upsert=True,
    )
    return conversation_id

async def append_message(user_id: str, conversation_id: str, message: Message) -> None:
    await db.chats.update_one(
        {"conversation_id": conversation_id},
        {"$setOnInsert": {"user_id": user_id, "conversation_id": conversation_id},
         "$push": {"messages": message.dict()}},
        upsert=True,
    )

async def get_chat(conversation_id: str) -> Optional[dict]:
    return await db.chats.find_one({"conversation_id": conversation_id}, {"_id": 0})

async def delete_chat(conversation_id: str) -> bool:
    res = await db.chats.delete_one({"conversation_id": conversation_id})
    return res.deleted_count == 1

async def list_chats_by_user(user_id: str, page: int = 1, limit: int = 10) -> tuple[list[dict], int]:
    skip = (page - 1) * limit
    cursor = db.chats.find({"user_id": user_id}, {"_id": 0}).skip(skip).limit(limit).sort("conversation_id")
    items = [doc async for doc in cursor]
    total = await db.chats.count_documents({"user_id": user_id})
    return items, total
