from typing import Optional

from operation import Operation
from pydantic import BaseModel

from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Structs import Initiator, Volume


class UpdateVolumeAccessGroupRequest(BaseModel):
    volumeAccessGroupId: str
    volumeAccessGroupName: str
    clusterId: str
    volumes: list[Volume]


class UpdateVolumeAccessGroupResponse(BaseModel):
    pass


class UpdateVolumeAccessGroupOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="v1/volume-access-groups",
            requester=RestRequest(method=Method.PUT).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: UpdateVolumeAccessGroupRequest) -> UpdateVolumeAccessGroupResponse:
        return super().invoke(request)

