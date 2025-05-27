# app/services/rag_service.py
import openai
from typing import List, Dict, Any
from app.models.chat import ChatRequest, ChatResponse, RelevantChunk
from app.services.vector_store import VectorStore
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.vector_store = VectorStore()
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        """Generate response using RAG"""
        # Retrieve relevant chunks
        similar_chunks = self.vector_store.search_similar_chunks(
            document_id=request.document_id,
            query=request.message,
            top_k=settings.TOP_K_CHUNKS
        )
        
        relevant_chunks = [
            RelevantChunk(
                text=chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                score=chunk['score'],
                chunk_id=chunk['id'],
                start_index=chunk['metadata'].get('start_index', 0),
                end_index=chunk['metadata'].get('end_index', 0)
            )
            for chunk in similar_chunks
        ]
        
        # Generate response
        if settings.OPENAI_API_KEY and similar_chunks:
            response_text = await self._generate_llm_response(request.message, similar_chunks)
        else:
            response_text = self._generate_fallback_response(request.message, similar_chunks)
        
        return ChatResponse(
            message=response_text,
            relevant_chunks=relevant_chunks
        )
    
    async def _generate_llm_response(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        """Generate response using OpenAI GPT"""
        context = "\n\n".join([chunk['text'] for chunk in chunks])
        
        prompt = f"""Based on the following context from the document, answer the user's question.

Context:
{context}

Question: {query}

Answer:"""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided document context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            return self._generate_fallback_response(query, chunks)
    
    def _generate_fallback_response(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        """Generate fallback response when LLM is not available"""
        if not chunks:
            return "I couldn't find relevant information in the document to answer your question. Please try rephrasing your query."
        
        # Simple keyword-based response
        context = chunks[0]['text']
        return f"Based on the document, here's what I found:\n\n{context[:300]}..."
