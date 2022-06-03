from pydantic import BaseModel

from operation.Operation import Operation
from request.Request import FormRequest


class LoginRequest(BaseModel):
    grant_type: str = "password"
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class LoginOperation(Operation):
    def __init__(self, host: str):
        from utils.Consts import HCD_AUTH
        super().__init__(
            host=host,
            path="/oauth/token",
            requester=FormRequest().add_header("Authorization", HCD_AUTH)
        )

    def invoke(self, request: LoginRequest) -> LoginResponse:
        return super().invoke(request)



