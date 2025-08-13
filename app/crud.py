from app.database import db
from bson import ObjectId

# Insert a new chat
async def create_chat(conversation_id: str, user_id: str, messages: list):
    chat_data = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "messages": messages
    }
    await db.chats.insert_one(chat_data)
    return chat_data

# Get a chat by conversation ID
async def get_chat(conversation_id: str):
    return await db.chats.find_one({"conversation_id": conversation_id})

# Get paginated chats for a user
async def get_user_chats(user_id: str, skip: int, limit: int):
    cursor = db.chats.find({"user_id": user_id}).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)

# Delete a chat
async def delete_chat(conversation_id: str):
    result = await db.chats.delete_one({"conversation_id": conversation_id})
    return result.deleted_count
