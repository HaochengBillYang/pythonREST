from typing import Optional

from operation import Operation
from pydantic import BaseModel

from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class CreateVolumeAccessGroupRequest(BaseModel):
    volumeAccessGroupName: str
    clusterId: str
    initiators: list[str]
    volumes: list[str]


class CreateVolumeAccessGroupResponse(BaseModel):
    pass


class IdWrapper(BaseModel):
    id: str


class CreateVolumeAccessGroupRequestWrapper(BaseModel):
    volumeAccessGroupName: str
    clusterId: str
    initiators: list[IdWrapper]
    volumes: list[IdWrapper]

    @staticmethod
    def transform(req: CreateVolumeAccessGroupRequest) -> "CreateVolumeAccessGroupRequestWrapper":
        return CreateVolumeAccessGroupRequestWrapper(
            volumeAccessGroupName=req.volumeAccessGroupName,
            clusterId=req.clusterId,
            initiators=list(map(lambda it: IdWrapper(id=it), req.initiators)),
            volumes=list(map(lambda it: IdWrapper(id=it), req.volumes)),
        )


class CreateVolumeAccessGroupOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/volume-access-groups",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: CreateVolumeAccessGroupRequest) -> CreateVolumeAccessGroupResponse:
        return super().invoke(CreateVolumeAccessGroupRequestWrapper.transform(request))


