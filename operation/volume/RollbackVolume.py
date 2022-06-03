from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import FormRequest, RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class RollbackVolumeRequest(BaseModel):
    clusterId: str
    volumeId: str
    snapshotId: str


class RollbackVolumeResponse(BaseModel):
    pass


class RollbackVolumeOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volumes/task/rollback",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: RollbackVolumeRequest) -> RollbackVolumeResponse:
        return super().invoke(request)

