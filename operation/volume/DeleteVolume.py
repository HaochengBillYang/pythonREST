from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import FormRequest, RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class DeleteVolumeRequest(BaseModel):
    clusterId: str
    byName: bool = False
    volumeIdOrNameList: list[str]
    force: bool = False


class DeleteVolumeResponse(BaseModel):
    pass

