import json
import os
from typing import Optional  # Data type of either None or inputed value

from pydantic import BaseModel

from operation.AccessKeyManager import AccessKeyManager
from request.Request import FormRequest, Request, RestRequest, Method, Pipeline
from request.pipelines.SimpleLogger import SimpleLogger
import importlib

from utils.DynamicLoader import DynamicLoader
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

loader = DynamicLoader(os.path.dirname(__file__))


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
            module_name = self.__class__.__name__.removesuffix("Operation")
            class_name = module_name + "Response"
            kclass = loader.load(module_name, class_name)
            results = response.return_data
            if results == "":
                results = {}
            else:
                results = json.loads(results)
            return kclass(**results)
        else:
            raise Exception("Status Error : " + response.return_data)
