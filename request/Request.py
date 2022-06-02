from enum import Enum

import requests as req


class Pipeline(object):
    def invoke_before_request(self, request: "Request"):
        pass

    def invoke_after_request(self, request: "Request", response: "Response"):
        pass


class Response(object):
    def __init__(self, return_code: int, return_data: str):
        self.return_code: int = return_code
        self.return_data: str = return_data


class Request(object):
    def __init__(self):
        self.url: str = ""
        self.path: str = ""
        self.host: str = ""
        self.headers: dict = {}
        self.data: dict = {}
        self.pipelines: list[Pipeline] = []

    def add_header(self, key: str, value: str) -> "Request":
        self.headers[key] = value
        return self

    def set_data(self, data: dict) -> "Request":
        self.data = data
        return self

    def add_data(self, key: str, value: str) -> "Request":
        self.data[key] = value
        return self

    def add_pipeline(self, pipeline: Pipeline) -> "Request":
        self.pipelines.append(pipeline)
        return self

    def send(self, host: str, path: str) -> Response:

        if host.endswith("/"):
            host = host.removesuffix("/")

        if path.startswith("/"):
            path = path.removeprefix("/")

        self.host = host
        self.path = path
        self.url = host + "/" + path
        return self._actual_send()

    def _actual_send(self) -> Response:
        pass

    def _before_request(self) -> None:
        for pipeline in self.pipelines:
            pipeline.invoke_before_request(self)

    def _after_request(self, response: Response) -> None:
        for pipeline in self.pipelines:
            pipeline.invoke_after_request(self, response)


class FormRequest(Request):
    def __init__(self):
        super().__init__()
        self.add_header("Content-Type", "application/x-www-form-urlencoded")

    def _actual_send(self) -> Response:
        self._before_request()
        resp = req.post(url=self.url, data=self.data, headers=self.headers, verify=False)
        response = Response(resp.status_code, resp.text)
        self._after_request(response)
        return response


class Method(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3
    PATCH = 4


class RestRequest(Request):
    def __init__(self, method: Method):
        super().__init__()
        self.method = method
        self.add_header("Content-Type", "application/json; charset=utf8")

    def _actual_send(self) -> Response:
        self._before_request()
        resp = None
        if self.method == Method.GET:
            print(self.data)
            resp = req.get(url=self.url, params=self.data, headers=self.headers, verify=False)
        elif self.method == Method.POST:
            resp = req.post(url=self.url, json=self.data, headers=self.headers, verify=False)
        elif self.method == Method.PUT:
            resp = req.put(url=self.url, json=self.data, headers=self.headers, verify=False)
        elif self.method == Method.DELETE:
            # If a DELETE request includes an entity body, the body is ignored
            resp = req.delete(url=self.url, data=self.data, headers=self.headers, verify=False)
        elif self.method == Method.PATCH:
            resp = req.patch(url=self.url, json=self.data, headers=self.headers, verify=False)

        response = Response(resp.status_code, resp.text)
        self._after_request(response)
        return response
