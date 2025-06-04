from transformers import T5ForConditionalGeneration, T5Tokenizer
import json, torch, os, functools
from fastapi import APIRouter
from pydantic import BaseModel

from ..services.taskify_service import extract_tasks 
router = APIRouter(prefix="/taskify", tags=["Taskify"])

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model     = T5ForConditionalGeneration.from_pretrained(
    os.getenv("TASKIFY_MODEL", "your‑fine‑tuned‑model")
).eval()

def extract_tasks(lines):
    prompt = "extract todos as json:\n" + "\n".join(lines)
    ids = tokenizer(prompt, return_tensors="pt").input_ids
    with torch.no_grad():
        outputs = model.generate(ids, max_length=256)
    raw_json = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return json.loads(raw_json)
