from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline


class UpdateInitiatorRequest(BaseModel):
    initiatorId: str
    iqn: str
    initiatorName: str


class UpdateInitiatorResponse(BaseModel):
    pass


class CreateInitiatorOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="v1/initiators",
            requester=RestRequest(method=Method.PUT).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: UpdateInitiatorRequest) -> UpdateInitiatorResponse:
        return super().invoke(request)



