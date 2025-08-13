from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

import crud
from models import Message
from summarizer import summarize_chat

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, conversation_id: str, websocket: WebSocket):
        await websocket.accept()
        self.rooms.setdefault(conversation_id, set()).add(websocket)

    def disconnect(self, conversation_id: str, websocket: WebSocket):
        if conversation_id in self.rooms:
            self.rooms[conversation_id].discard(websocket)
            if not self.rooms[conversation_id]:
                del self.rooms[conversation_id]

    async def broadcast(self, conversation_id: str, data: dict):
        if conversation_id not in self.rooms:
            return
        dead = []
        payload = json.dumps(data)
        for ws in list(self.rooms[conversation_id]):
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(conversation_id, ws)

manager = ConnectionManager()

@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    await manager.connect(conversation_id, websocket)
    try:
        await manager.broadcast(conversation_id, {"type": "status", "message": "connected"})
        while True:
            text = await websocket.receive_text()
            # Client should send: {"user_id":"u1","sender_id":"u1","message":"hi"}
            try:
                data = json.loads(text)
                user_id = data.get("user_id", "unknown")
                msg = Message(sender_id=data.get("sender_id", user_id), message=data.get("message", ""))
            except Exception:
                await websocket.send_text(json.dumps({"type": "error", "message": "Invalid JSON"}))
                continue

            await crud.append_message(user_id, conversation_id, msg)
            chat = await crud.get_chat(conversation_id)
            summary, keywords, sentiment = summarize_chat(chat.get("messages", []))

            await manager.broadcast(conversation_id, {
                "type": "update",
                "conversation_id": conversation_id,
                "messages": len(chat.get("messages", [])),
                "summary": summary,
                "keywords": keywords,
                "sentiment": sentiment
            })
    except WebSocketDisconnect:
        manager.disconnect(conversation_id, websocket)
