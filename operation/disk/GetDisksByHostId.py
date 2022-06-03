# get_disks_by_host_id
from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Utils import CustomBase


class GetDisksByHostIdRequest(CustomBase):
    hostId: str

    class Config:
        exclude = {"hostId"}


class DiskInfo(BaseModel):
    diskId: str
    mountPoint: str
    hostId: str
    state: str
    diskTagList: list[str]


class GetDisksByHostIdResponse(BaseModel):
    data: list[DiskInfo]


class GetDisksByHostIdOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/disks/by-host/",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetDisksByHostIdRequest) -> GetDisksByHostIdResponse:
        self.path += request.hostId
        return super().invoke(request)
