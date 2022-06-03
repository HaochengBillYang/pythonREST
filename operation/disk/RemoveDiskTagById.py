from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Utils import CustomBase


class RemoveDiskTagByIdRequest(CustomBase):
    hostId: str
    diskIds: list[str]
    diskTag: str

    class Config:
        exclude = {"hostId", "diskIds"}


class RemoveDiskTagByIdResponse(BaseModel):
    taskId: str
    pass


class RemoveDiskTagByIdOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/disks/tag/auto-disable/",
            requester=RestRequest(method=Method.DELETE).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: RemoveDiskTagByIdRequest) -> RemoveDiskTagByIdResponse:
        if len(request.diskIds) == 0:
            raise Exception("Can not have zero length diskIds")

        self.path += request.hostId
        self.path += "/"
        self.path += ",".join(request.diskIds)
        self.path += "/"
        self.path += request.diskTag
        return super().invoke(request)
