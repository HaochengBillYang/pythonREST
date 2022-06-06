# getAllClusters
from typing import Optional

from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class CreateClusterInfo(BaseModel):
    clusterName: str
    minClusterSize: int
    replicationFactor: int
    virtualIp: str
    storageVirtualIpv6: Optional[str]


class CreateClusterRequest(BaseModel):
    cluster: CreateClusterInfo
    hosts: Optional[list[str]]
    pass


class CreateClusterResponse(BaseModel):
    pass


class CreateClusterOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/clusters",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: CreateClusterRequest) -> CreateClusterResponse:
        return super().invoke(request)
