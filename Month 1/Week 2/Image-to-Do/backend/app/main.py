from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import ocr, taskify, export

from routes import ocr, taskify, export

app = FastAPI(title="Image‑to‑Do API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev‑friendly
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router)
app.include_router(taskify.router)
app.include_router(export.router)
