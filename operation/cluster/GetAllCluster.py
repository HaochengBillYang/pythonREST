# getAllClusters
from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class GetAllClustersRequest(BaseModel):
    pass


class ClusterInfo(BaseModel):
    clusterId: str
    clusterName: str
    state: str
    type: str


class GetAllClustersResponse(BaseModel):
    data: list[ClusterInfo]
    pass


class GetAllClustersOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/clusters",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetAllClustersRequest) -> GetAllClustersResponse:
        return super().invoke(request)
