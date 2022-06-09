from typing import Optional

from operation import Operation
from pydantic import BaseModel

from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Utils import CustomBase


class DeleteVolumeAccessGroupRequest(CustomBase):
    volumeAccessGroupId: str
    clusterId: str

    class Config:
        exclude = {"volumeAccessGroupName", "clusterId"}


class DeleteVolumeAccessGroupResponse(BaseModel):
    pass


class DeleteVolumeAccessGroupOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="v1/volume-access-groups/",
            requester=RestRequest(method=Method.DELETE).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: DeleteVolumeAccessGroupRequest) -> DeleteVolumeAccessGroupResponse:
        self.path += request.clusterId + "/" + request.volumeAccessGroupId
        return super().invoke(request)



