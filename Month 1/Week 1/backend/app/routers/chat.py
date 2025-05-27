# app/routers/chat.py
from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.rag_service import RAGService

router = APIRouter()

rag_service = RAGService()

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """Process chat query and return response"""
    try:
        response = await rag_service.generate_response(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")