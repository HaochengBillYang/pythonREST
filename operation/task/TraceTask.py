from typing import Optional
from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Utils import CustomBase


class TraceTaskRequest(CustomBase):
    taskId: str

    class Config:
        exclude = {"taskId"}


class TraceTaskResponse(BaseModel):
    progress: int
    taskName: str
    statusName: Optional[str]
    resourcesId: str
    completeTime: int
    startTime: int


class TraceTaskOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/task/",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: TraceTaskRequest) -> TraceTaskResponse:
        self.path += request.taskId
        return super().invoke(request)

