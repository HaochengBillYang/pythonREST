from typing import Optional

from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class CheckRollbackVolumeRequest(BaseModel):
    clusterId: str
    volumeId: str


class CheckRollbackVolumeResponse(BaseModel):
    pass


class CheckRollbackVolumeOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volumes/rollback-status",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: CheckRollbackVolumeRequest) -> CheckRollbackVolumeResponse:
        return super().invoke(request)
