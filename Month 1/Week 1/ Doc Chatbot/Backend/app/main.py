from uuid import uuid4
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .deps import extract_text_from_file, chunk_text
from .rag import ingest_doc, ask_rag, summarize_rag

app = FastAPI(title="Doc‑Chatbot")

# ──────────────────────────────────────────────
# CORS so the Vite dev‑server can talk to us
# ──────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In‑memory “DB” → workspace‑id ➜ vector‑store
WORKSPACES: dict[str, any] = {}

# ───────────────────────────
# Schemas
# ───────────────────────────
class UploadResp(BaseModel):
    workspace_id: str


class ChatReq(BaseModel):
    workspace_id: str
    question: str


class SummReq(BaseModel):
    workspace_id: str
    section_title: str | None = ""


class SummResp(BaseModel):
    summary: str


# ───────────────────────────
# Routes
# ───────────────────────────
@app.post("/upload", response_model=UploadResp)
async def upload(file: UploadFile = File(...)):
    """User drops a PDF -> return workspace‑id."""
    raw = await file.read()
    text = extract_text_from_file(file.filename, raw)
    docs = chunk_text(text)                          # list[Document]
    ws_id = str(uuid4())
    WORKSPACES[ws_id] = ingest_doc(docs)             # store vector‑store
    return {"workspace_id": ws_id}


@app.post("/chat")
async def chat(data: ChatReq):
    """Stream an answer – Server‑Sent Events."""
    stream = ask_rag(WORKSPACES[data.workspace_id], data.question)

    async def event_stream():
        for chunk in stream:                         # generator from rag.py
            yield f"data: {chunk}\n\n"

    return StreamingResponse(event_stream(),
                             media_type="text/event-stream")


@app.post("/summarize", response_model=SummResp)
async def summarize(data: SummReq):
    """Return one‑shot summary of a section (or whole doc)."""
    summary = summarize_rag(
        WORKSPACES[data.workspace_id],
        data.section_title or "",
    )
    return {"summary": summary}
