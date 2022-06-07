from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Structs import DiskInfo
from utils.Utils import CustomBase


class GetDisksByClusterRequest(CustomBase):
    clusterId: str

    class Config:
        exclude = {"hostId"}


class GetDisksByClusterResponse(CustomBase):
    data: list[DiskInfo]


class GetDisksByClusterOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/disks/",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetDisksByClusterRequest) -> GetDisksByClusterResponse:
        self.path += request.clusterId
        return super().invoke(request)
