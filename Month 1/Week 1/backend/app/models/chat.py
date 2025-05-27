# app/models/chat.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = datetime.now()

class ChatRequest(BaseModel):
    document_id: str
    message: str
    chat_history: List[ChatMessage] = []

class RelevantChunk(BaseModel):
    text: str
    score: float
    chunk_id: str
    start_index: int
    end_index: int

class ChatResponse(BaseModel):
    message: str
    relevant_chunks: List[RelevantChunk]
    timestamp: datetime = datetime.now()