from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Chat message schema
class ChatMessage(BaseModel):
    sender_id: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Chat schema for storing in DB
class Chat(BaseModel):
    conversation_id: str
    user_id: str
    messages: List[ChatMessage]

# Schema for creating new chats
class ChatCreate(BaseModel):
    user_id: str
    messages: List[ChatMessage]

# Schema for summarization request
class SummarizeRequest(BaseModel):
    conversation_id: str

# Schema for summarization response
class SummarizeResponse(BaseModel):
    summary: str
    keywords: Optional[List[str]] = None
    sentiment: Optional[str] = None
