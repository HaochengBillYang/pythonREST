from datetime import datetime
from enum import Enum

from request.Request import Request, Response, Pipeline


class ColorCode(Enum):
    GREEN = 1
    RED = 2
    BLUE = 3
    RESET = 99

    def to_code(self) -> str:
        if self == ColorCode.GREEN:
            return "\033[32m"
        elif self == ColorCode.RED:
            return "\033[31m"
        elif self == ColorCode.BLUE:
            return "\033[36m"
        elif self == ColorCode.RESET:
            return "\033[0m"
        raise "Never Happen"


class SimpleLogger(Pipeline):
    def __init__(self, logger_name: str):
        self.logger_name = logger_name

    def logger(self, color: ColorCode, message: str) -> None:
        now = datetime.now()
        date_time = now.strftime("[%m/%d-%H:%M:%S]: ")
        print(color.to_code(), date_time, message)

    def invoke_before_request(self, request: Request):
        self.logger(ColorCode.BLUE, "Requesting " + request.url + " ;data = " + str(request.data))

    def invoke_after_request(self, request: Request, response: Response):
        self.logger(ColorCode.GREEN, "Response From " + request.url + " ;code = " + str(
            response.return_code) + " ;data = " + response.return_data)
