from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import FormRequest, RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class ExtendVolumeRequest(BaseModel):
    clusterId: str
    volumeId: str
    volumeName: str
    volumeNumericalId: int
    volumeSize: int


class ExtendVolumeResponse(BaseModel):
    pass


class ExtendVolumeOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volumes/extend",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: ExtendVolumeRequest) -> ExtendVolumeResponse:
        return super().invoke(request)

