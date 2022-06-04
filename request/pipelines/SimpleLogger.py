from datetime import datetime

from request.Request import Request, Response, Pipeline
from utils.Logging import ColorCode


class SimpleLogger(Pipeline):
    def __init__(self, logger_name: str):
        self.logger_name = logger_name

    def logger(self, color: ColorCode, message: str) -> None:
        now = datetime.now()
        date_time = now.strftime("%m/%d-%H:%M:%S]")
        print(color.to_code() + "[" + self.logger_name, date_time + message, ColorCode.RESET.to_code())

    def invoke_before_request(self, request: Request):
        self.logger(ColorCode.BLUE, " >> " + request.path + " ;data = " + str(request.data))

    def invoke_after_request(self, request: Request, response: Response):
        self.logger(ColorCode.GREEN, " << " + request.path + " ;code = " + str(
            response.return_code) + " ;data = " + response.return_data)
