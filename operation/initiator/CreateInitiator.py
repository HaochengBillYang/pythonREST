from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class CreateInitiatorRequest(BaseModel):
    iqn: str
    initiatorName: str


class CreateInitiatorResponse(BaseModel):
    pass


class CreateInitiatorOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="v1/initiators",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: CreateInitiatorRequest) -> CreateInitiatorResponse:
        return super().invoke(request)



