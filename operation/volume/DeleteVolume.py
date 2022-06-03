from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import FormRequest, RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class DeleteVolumeRequest(BaseModel):
    clusterId: str
    byName: bool = False
    volumeIdOrNameList: list[str]
    force: bool = False


class DeleteVolumeResponse(BaseModel):
    pass

class DeleteVolumeOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volumes/multi-delete",
            requester=RestRequest(method=Method.DELETE).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: DeleteVolumeRequest) -> DeleteVolumeResponse:
        return super().invoke(request)

