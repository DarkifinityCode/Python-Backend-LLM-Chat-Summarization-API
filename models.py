from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    sender_id: str = Field(..., description="ID of the sender (user/bot)")
    message: str = Field(..., description="Text content")
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ChatCreate(BaseModel):
    user_id: str
    conversation_id: Optional[str] = None
    messages: List[Message]

class ChatOut(BaseModel):
    user_id: str
    conversation_id: str
    messages: List[Message]

class SummarizeRequest(BaseModel):
    conversation_id: str

class SummarizeResponse(BaseModel):
    summary: str
    keywords: List[str]
    sentiment: str

class PaginatedChats(BaseModel):
    items: List[ChatOut]
    page: int
    limit: int
    total: int

class InsightsResponse(BaseModel):
    conversation_id: str
    message_count: int
    participant_count: int
    participants: List[str]
    avg_chars_per_message: float
    first_timestamp: Optional[str]
    last_timestamp: Optional[str]
    keywords: List[str]
    sentiment: str
