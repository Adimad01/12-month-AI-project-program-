from fastapi import APIRouter, File, UploadFile
from app.services.ocr_service import run_ocr

router = APIRouter()

@router.post("/ocr")
async def ocr_endpoint(img: UploadFile = File(...)):
    text = await run_ocr(img)
    return {"lines": text.split("\n")}
