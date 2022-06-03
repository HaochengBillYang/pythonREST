from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import FormRequest, RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class RenameVolumeRequest(BaseModel):
    clusterId: str
    volumeId: str
    volumeName: str ## new name


class RenameVolumeResponse(BaseModel):
    pass


class RenameVolumeOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volumes",
            requester=RestRequest(method=Method.PUT).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: RenameVolumeRequest) -> RenameVolumeResponse:
        return super().invoke(request)

    