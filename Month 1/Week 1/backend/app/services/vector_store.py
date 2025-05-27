# app/services/vector_store.py
import chromadb
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from app.models.document import Document, DocumentChunk
from app.core.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collections = {}
    
    def create_document_collection(self, document_id: str) -> None:
        """Create a new collection for a document"""
        collection_name = f"doc_{document_id}"
        collection = self.client.create_collection(
            name=collection_name,
            metadata={"document_id": document_id}
        )
        self.collections[document_id] = collection
    
    def add_document_chunks(self, document: Document) -> None:
        """Add document chunks to vector store"""
        if document.id not in self.collections:
            self.create_document_collection(document.id)
        
        collection = self.collections[document.id]
        
        # Prepare data for batch insertion
        texts = [chunk.text for chunk in document.chunks]
        embeddings = self.embedding_model.encode(texts).tolist()
        
        ids = [chunk.id for chunk in document.chunks]
        metadatas = [
            {
                "chunk_id": chunk.id,
                "start_index": chunk.start_index,
                "end_index": chunk.end_index,
                "document_id": document.id
            }
            for chunk in document.chunks
        ]
        
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search_similar_chunks(self, document_id: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar chunks in document"""
        if document_id not in self.collections:
            collection_name = f"doc_{document_id}"
            try:
                collection = self.client.get_collection(collection_name)
                self.collections[document_id] = collection
            except:
                return []
        
        collection = self.collections[document_id]
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        similar_chunks = []
        for i in range(len(results['ids'][0])):
            similar_chunks.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i],
                'score': 1 - results['distances'][0][i],  # Convert distance to similarity
                'metadata': results['metadatas'][0][i]
            })
        
        return similar_chunks
    
    def delete_document_collection(self, document_id: str) -> None:
        """Delete document collection"""
        collection_name = f"doc_{document_id}"
        try:
            self.client.delete_collection(collection_name)
            if document_id in self.collections:
                del self.collections[document_id]
        except:
            pass