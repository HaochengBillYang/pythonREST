# give_disk_tag_by_id
from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class GiveDiskTagByIdRequest(BaseModel):
    hostId: str
    diskIds: list[str]
    diskTag: str


class GiveDiskTagByIdResponse(BaseModel):
    pass


class GiveDiskTagByIdOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/disks/tag/auto-enable",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GiveDiskTagByIdRequest) -> GiveDiskTagByIdResponse:
        return super().invoke(request)
