from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Structs import Initiator


class GetInitiatorRequest(BaseModel):
    pass


class GetInitiatorResponse(BaseModel):
    data: list[Initiator]
    pass


class CreateInitiatorOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="v1/initiators",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetInitiatorRequest) -> GetInitiatorResponse:
        return super().invoke(request)


