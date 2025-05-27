# app/models/document.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    name: str
    file_type: str
    size: int

class DocumentCreate(DocumentBase):
    pass

class DocumentChunk(BaseModel):
    id: str
    text: str
    start_index: int
    end_index: int
    metadata: dict = {}

class Document(DocumentBase):
    id: str
    upload_date: datetime
    chunks: List[DocumentChunk] = []
    text_content: Optional[str] = None
    
    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: str
    name: str
    file_type: str
    size: int
    upload_date: datetime
    chunk_count: int
