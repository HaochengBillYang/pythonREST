import json
from typing import Optional

from pydantic import BaseModel

from operation.AccessKeyManager import AccessKeyManager
from request.Request import FormRequest, Request, RestRequest, Method, Pipeline
from request.pipelines.SimpleLogger import SimpleLogger
from utils.Utils import SingletonObject, CustomBase


# All operation must present in operation.py, stack from top to down #


# 1: BaseModel and CustomBase
# objects extends BaseModel or CustomBase provide strictly typed Json serialization, every field must declare type
# default value and Optional[type] are supported

# CustomBase provide the ability to exclude some field from serialization, this could be useful when it comes
# to parameter in the path, refer to RemoveDiskTagByIdOperation


# 2: Operation Lifecycle
# stage I: Operation created, every operation is stateless, so you MUST provide host for every information
# stage II: invoke is called with the corresponding Request object.
# stage III: actual request are built within invoke method, and request (or requests) will be executed by requester

# Requester stage I: allocate Host, Port and Path
# Requester stage II: every pipeline are called with invoke_before_request
# Requester stage III: actual request sent, and after response received
# Requester stage IV: every pipeline are called with invoke_after_request

# stage IV: an object named ```self.__class__.__name__.removesuffix("Operation") + "Response"``` will be created
# stage V: data from requester will be parsed to the Response object, strictly typed
#
# You can mark Operation objects as SingletonObject, but it may affect IDE behavior(type hint and auto complete)


# 3:Pipelines:
# pipelines are called before and after actual HTTP request, pipelines can modify request/response object
# Typical usage of pipeline: SimpleLogger and KeyExchangePipeline(down below)


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
            results = response.return_data
            if results == "":
                results = {}
            else:
                results = json.loads(results)
            return kclass(**results)
        else:
            raise Exception("Status Error : " + response.return_data)


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


# give_disk_tag_by_id
class GiveDiskTagByIdRequest(BaseModel):
    hostId: str
    diskIds: list[str]
    diskTag: str


class GiveDiskTagByIdResponse(BaseModel):
    pass


class GiveDiskTagByIdOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/disks/tag/auto-enable",
            requester=RestRequest(method=Method.POST).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: GiveDiskTagByIdRequest) -> GiveDiskTagByIdResponse:
        return super().invoke(request)


# remove_disk_tag_by_id
class RemoveDiskTagByIdRequest(CustomBase):
    hostId: str
    diskIds: list[str]
    diskTag: str

    class Config:
        exclude = {"hostId", "diskIds"}


class RemoveDiskTagByIdResponse(BaseModel):
    taskId: str
    pass


class RemoveDiskTagByIdOperation(Operation):
    def __init__(self, host: str):
        super().__init__(
            host=host,
            path="/v1/disks/tag/auto-disable/",
            requester=RestRequest(method=Method.DELETE).add_pipeline(KeyExchangePipeline())
        )

    def invoke(self, request: RemoveDiskTagByIdRequest) -> RemoveDiskTagByIdResponse:
        if len(request.diskIds) == 0:
            raise Exception("Can not have zero length diskIds")

        self.path += request.hostId
        self.path += "/"
        self.path += ",".join(request.diskIds)
        self.path += "/"
        self.path += request.diskTag
        return super().invoke(request)
