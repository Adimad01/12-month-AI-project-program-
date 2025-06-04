from fastapi import APIRouter, UploadFile, File
from ..services.ocr_service import run_ocr

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("")
async def ocr_endpoint(img: UploadFile = File(...)):
    text_lines = await run_ocr(img)
    return {"text": text_lines}
