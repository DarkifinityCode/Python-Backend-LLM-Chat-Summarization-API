from fastapi import APIRouter, Query
from models import PaginatedChats
import crud

router = APIRouter()

@router.get("/{user_id}/chats", response_model=PaginatedChats)
async def list_user_chats(user_id: str, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    items, total = await crud.list_chats_by_user(user_id, page=page, limit=limit)
    return {"items": items, "page": page, "limit": limit, "total": total}
