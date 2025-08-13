from fastapi import APIRouter
from app import crud

router = APIRouter()

@router.get("/{user_id}/chats")
async def get_user_chats(user_id: str, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit
    chats = await crud.get_user_chats(user_id, skip, limit)
    return {"user_id": user_id, "page": page, "chats": chats}
