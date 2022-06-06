from typing import Optional

from operation import Operation
from pydantic import BaseModel

from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Structs import Initiator, Volume


class CreateVolumeAccessGroupRequest(BaseModel):
    volumeAccessGroupName: str
    clusterId: str
    initiators: list[Initiator]
    volumes: list[Volume]


class CreateVolumeAccessGroupResponse(BaseModel):
    pass


class CreateVolumeAccessGroupOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volume-access-groups",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: CreateVolumeAccessGroupRequest) -> CreateVolumeAccessGroupResponse:
        return super().invoke(request)


