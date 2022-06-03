from typing import Optional
from pydantic import BaseModel
from utils.Utils import CustomBase


class TraceTaskRequest(CustomBase):
    taskId: str


class TraceTaskResponse(BaseModel):
    progress: int
    taskName: str
    statusName: Optional[str]
    resourcesId: str
    completeTime: int
    startTime: int



