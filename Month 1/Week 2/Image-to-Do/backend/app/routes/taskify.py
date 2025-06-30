from fastapi import APIRouter
from pydantic import BaseModel
from ..services.taskify_service import extract_tasks

router = APIRouter(prefix="/taskify", tags=["Taskify"])

class TaskifyIn(BaseModel):
    lines: list[str]

@router.post("")
async def taskify(data: TaskifyIn):
    tasks = extract_tasks(data.lines)
    return {"tasks": tasks}
