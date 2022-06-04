from time import sleep
from typing import Optional
from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Utils import CustomBase


class TraceUntilCompleteRequest(CustomBase):
    taskId: str

    class Config:
        exclude = {"taskId"}


class TraceUntilCompleteResponse(BaseModel):
    progress: int
    taskName: str
    statusName: Optional[str]
    resourceId: str
    completeTime: int
    startTime: int


class TraceUntilCompleteOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/tasks/",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: TraceUntilCompleteRequest) -> TraceUntilCompleteResponse:
        self.path += request.taskId
        while True:
            response = super().invoke(request)

            if response.progress == 100:
                return response
            else:
                sleep(2)
