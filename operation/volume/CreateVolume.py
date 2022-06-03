from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import FormRequest, RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class CreateVolumeRequest(BaseModel):
    volumeName: str
    clusterId: str
    volumeSize: int
    blockSize: int = 4096
    type: str = "NORMAL"


class CreateVolumeResponse(BaseModel):
    pass


class CreateVolumeOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volumes/task/create",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: CreateVolumeRequest) -> CreateVolumeResponse:
        return super().invoke(request)