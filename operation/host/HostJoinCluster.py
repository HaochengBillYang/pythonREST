from typing import Optional

from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class HostJoinClusterRequest(BaseModel):
    clusterId: str
    hosts: list[str]
    pass


class HostJoinClusterResponse(BaseModel):
    pass


class HostJoinClusterOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/hosts/join",
            requester=RestRequest(method=Method.PUT).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: HostJoinClusterRequest) -> HostJoinClusterResponse:
        return super().invoke(request)
