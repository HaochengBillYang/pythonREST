from typing import Optional

from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class HostLeaveClusterRequest(BaseModel):
    clusterId: str
    hosts: list[str]
    force: bool = False
    pass


class HostLeaveClusterResponse(BaseModel):
    pass


class HostLeaveClusterOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/hosts/leave",
            requester=RestRequest(method=Method.PUT).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: HostLeaveClusterRequest) -> HostLeaveClusterResponse:
        return super().invoke(request)
