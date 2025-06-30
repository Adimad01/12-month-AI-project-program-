"""
Minimal RAG helpers for chat + section summary.
Requires:  pip install ollama sentence-transformers
"""
from typing import Generator, List
import logging

import ollama           # pip install ollama
from langchain.docstore.document import Document
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

log = logging.getLogger(__name__)
MODEL = "llama3"         # or whatever you pulled


# ─────────────────────────────────────────
# Build vector store from list[Document]
# ─────────────────────────────────────────
def ingest_doc(docs: List[Document]) -> FAISS:
    emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(docs, emb)


# ─────────────────────────────────────────
# Chat – yields chunks (used for streaming)
# ─────────────────────────────────────────
def ask_rag(store: FAISS, question: str) -> Generator[str, None, None]:
    log.info("RAG Question: %s", question)

    # Grab top‑k
    docs = store.similarity_search(question, k=5)
    log.info("Found %d relevant documents", len(docs))

    context = "\n\n".join(d.page_content for d in docs)
    prompt = (
        "You are an AI assistant helping a user understand a PDF.\n\n"
        f"Context:\n{context}\n\nUser: {question}\nAssistant:"
    )

    # stream=True returns an iterator of dicts
    for chunk in ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    ):
        yield chunk["message"]["content"]


# ─────────────────────────────────────────
# One‑shot summarisation (no streaming)
# ─────────────────────────────────────────
def summarize_rag(store: FAISS, section_title: str = "") -> str:
    """Return a paragraph‑length summary."""
    if section_title:
        docs = store.similarity_search(section_title, k=8)
    else:  # summarise whole doc
        docs = store.similarity_search("", k=12)

    context = "\n\n".join(d.page_content for d in docs)
    prompt = (
        "Provide a concise, beginner‑friendly summary "
        f"of the section titled '{section_title or 'whole document'}'.\n\n"
        f"Content:\n{context}\n\nSummary:"
    )

    res = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    return res["message"]["content"].strip()
