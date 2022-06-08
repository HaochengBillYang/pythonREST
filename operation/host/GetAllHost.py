# getAllHost
from typing import Optional

from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Structs import HostInfo


class GetAllHostRequest(BaseModel):
    onlyFreeHost: Optional[bool]
    clusterId: Optional[str]
    pass



class GetAllHostResponse(BaseModel):
    data: list[HostInfo]
    pass


class GetAllHostOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/hosts",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetAllHostRequest) -> GetAllHostResponse:
        return super().invoke(request)
