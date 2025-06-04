from fastapi import APIRouter
from pydantic import BaseModel
from ..services.integrations import send_to_todoist, send_to_google_tasks
from fastapi import APIRouter
from pydantic import BaseModel

from ..services.integrations import send_to_todoist, send_to_google_tasks  # ← relative

router = APIRouter(prefix="/export", tags=["Export"])

class ExportIn(BaseModel):
    provider: str  # 'todoist' | 'google'
    tasks: list[dict]

@router.post("")
async def export_tasks(payload: ExportIn):
    if payload.provider == "todoist":
        send_to_todoist(payload.tasks)
    elif payload.provider == "google":
        send_to_google_tasks(payload.tasks)
    else:
        return {"error": "unknown provider"}
    return {"status": "ok"}
