# ocr_service.py

from transformers import AutoModel, AutoTokenizer
import torch
import tempfile
import shutil
import os
from fastapi import UploadFile

MODEL_NAME = "stepfun-ai/GOT-OCR2_0"

# 1) On charge le tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

# 2) On charge le modèle en float32 sur CPU, sans essayer d'utiliser CUDA
model = AutoModel.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    torch_dtype=torch.float32,
    device_map={"": "cpu"}
).eval()


async def run_ocr(image_file: UploadFile) -> str:
    """
    Effectue l'OCR GOT-OCR2_0 sur une image reçue via FastAPI (CPU uniquement).
    :param image_file: fichier UploadFile envoyé depuis le client
    :return: texte détecté (chaîne complète, lignes séparées par '\n')
    """
    # 1) Sauvegarde temporaire du fichier reçu
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        shutil.copyfileobj(image_file.file, tmp)
        tmp_path = tmp.name

    try:
        # 2) On appelle exactement comme dans l'exemple :
        #    model.chat(tokenizer, "image.jpg", ocr_type="ocr")
        result = model.chat(tokenizer, tmp_path, ocr_type="ocr")

        # 3) GOT-OCR renvoie normalement un bloc de texte avec des sauts de ligne
        return result.strip()

    finally:
        # 4) On supprime le fichier temporaire
        os.remove(tmp_path)
