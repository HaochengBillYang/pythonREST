from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import RestRequest, Method
from request.pipelines.KeyExchange import KeyExchangePipeline
from utils.Utils import CustomBase


class DeleteInitiatorRequest(CustomBase):
    id: str

    class Config:
        exclude = {"id"}


class DeleteInitiatorResponse(BaseModel):
    pass


class DeleteInitiatorOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="v1/initiators/",
            requester=RestRequest(method=Method.DELETE).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: DeleteInitiatorRequest) -> DeleteInitiatorResponse:
        self.path += request.id
        return super().invoke(request)



