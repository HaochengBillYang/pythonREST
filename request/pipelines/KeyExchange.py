from operation.AccessKeyManager import AccessKeyManager
from operation.login.Login import LoginOperation, LoginRequest
from request.Request import Pipeline, Request


class KeyExchangePipeline(Pipeline):
    def invoke_before_request(self, request: Request):
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

