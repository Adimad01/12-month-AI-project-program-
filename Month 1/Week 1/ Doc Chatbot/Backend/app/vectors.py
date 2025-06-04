from sentence_transformers import SentenceTransformer
import faiss, numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter

class InMemoryVectorStore:
    _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def __init__(self):
        self.texts, self.metadatas = [], []
        self.index = faiss.IndexFlatL2(384)  # dim model
    def add_document(self, raw_text: str, metadata: dict):
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        for chunk in splitter.split_text(raw_text):
            emb = InMemoryVectorStore._model.encode([chunk])
            self.index.add(np.array(emb, dtype="float32"))
            self.texts.append(chunk)
            self.metadatas.append(metadata)
    def similarity_search(self, query: str, k: int = 6):
        emb = InMemoryVectorStore._model.encode([query])
        scores, idx = self.index.search(np.array(emb, dtype="float32"), k)
        return [(self.texts[i], self.metadatas[i], float(scores[0][j]))
                for j, i in enumerate(idx[0]) if i != -1]
