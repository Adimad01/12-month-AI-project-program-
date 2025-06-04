import cv2
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import io, torch

processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten").eval()

async def run_ocr(upload):
    img_bytes = await upload.read()
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    # (optional) deskew/resize with OpenCV here …
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    with torch.no_grad():
        generated_ids = model.generate(pixel_values)
    result = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return [ln.strip() for ln in result.split("\n") if ln.strip()]
