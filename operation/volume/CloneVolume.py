from typing import Optional

from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class CloneVolumeRequest(BaseModel):
    clusterId: str
    volumeId: str
    parentSnapshotId: str
    type: Optional[str]


class CloneVolumeResponse(BaseModel):
    pass


class CloneVolumeOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volumes/task/clone",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: CloneVolumeRequest) -> CloneVolumeResponse:
        return super().invoke(request)
