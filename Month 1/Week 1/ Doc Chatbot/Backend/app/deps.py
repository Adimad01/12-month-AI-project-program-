import io
import fitz              # PyMuPDF
import pytesseract
from PIL import Image
from langchain.docstore.document import Document
from textwrap import wrap

def extract_text_from_file(name: str, raw: bytes) -> str:
    if name.lower().endswith(".pdf"):
        pdf = fitz.open(stream=raw, filetype="pdf")
        return "\n".join(page.get_text() for page in pdf)
    raise ValueError("Only PDF supported.")

def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200):
    """Simple splitter that returns list[Document]."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        slice_ = text[start:end]
        meta = {"start": start, "end": end}
        chunks.append(Document(page_content=slice_, metadata=meta))
        start = end - overlap
    return chunks
