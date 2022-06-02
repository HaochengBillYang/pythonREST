import json
from typing import Optional

from pydantic import BaseModel

from operation.AccessKeyManager import AccessKeyManager
from request.Request import FormRequest, Request, Pipeline, RestRequest, Method
from request.pipelines.SimpleLogger import SimpleLogger
from utils.Utils import SingletonObject, CustomBase


class Operation:
    def __init__(self, host: str, path: str, requester: Request):
        self.host = host
        self.path = path
        self.requester: Request = requester

    def invoke(self, request):
        data = request.dict()
        # do not send optional values when it is null
        for k in data.keys():
            if data[k] is not None:
                self.requester.add_data(k, data[k])

        response = self.requester \
            .add_pipeline(SimpleLogger(self.__class__.__name__)) \
            .send(self.host, self.path)

        if response.return_code < 400:
            kclass = globals()[self.__class__.__name__.removesuffix("Operation") + "Response"]
            return kclass(**(json.loads(response.return_data)))
        else:
            raise Exception("Status Error")


# Login
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


# KeyExchangePipeline
class KeyExchangePipeline(Pipeline):
    def invoke_before_request(self, request: "Request"):
        key = AccessKeyManager.findAccessKeyByHost(request.host)
        if key is None:
            login_result = LoginOperation(host=request.host).invoke(
                LoginRequest(username="admin", password="Hello123!")
            )
            AccessKeyManager.addAccessKey(host=request.host,
                                          key_string=login_result.token_type + login_result.access_token,
                                          key_expire_in=login_result.expires_in)
            key = AccessKeyManager.findAccessKeyByHost(request.host)
        if key is None:
            raise Exception("Failed to find access key for host " + request.host)
        request.add_header("Authorization", key.key)


# getAllClusters
class GetAllClustersRequest(BaseModel):
    pass


class ClusterInfo(BaseModel):
    clusterId: str
    clusterName: str
    state: str
    type: str


class GetAllClustersResponse(BaseModel):
    data: list[ClusterInfo]
    pass


class GetAllClustersOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/clusters",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetAllClustersRequest) -> GetAllClustersResponse:
        return super().invoke(request)


# getAllHost
class GetAllHostRequest(BaseModel):
    onlyFreeHost: Optional[bool]
    clusterId: Optional[str]
    pass


class HostInfo(BaseModel):
    hostId: str
    hostName: str
    state: str


class GetAllHostResponse(BaseModel):
    data: list[HostInfo]
    pass


class GetAllHostOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/hosts",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetAllHostRequest) -> GetAllHostResponse:
        return super().invoke(request)


# get_disks_by_host_id
class GetDisksByHostIdRequest(CustomBase):
    hostId: str

    class Config:
        exclude = {"hostId"}


class DiskInfo(BaseModel):
    diskId: str
    mountPoint: str
    hostId: str
    state: str
    diskTagList: list[str]


class GetDisksByHostIdResponse(BaseModel):
    data: list[DiskInfo]


class GetDisksByHostIdOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/disks/by-host/",
            requester=RestRequest(method=Method.GET).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GetDisksByHostIdRequest) -> GetDisksByHostIdResponse:
        self.path += request.hostId
        return super().invoke(request)