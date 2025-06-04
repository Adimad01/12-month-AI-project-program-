# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importations relatives corrigées
from .routes import ocr, taskify, export

app = FastAPI()

# Exemple basique de gestion CORS (tu peux adapter si nécessaire)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr.router)
app.include_router(taskify.router)
app.include_router(export.router)

@app.get("/")
async def root():
    return {"message": "API is running"}
