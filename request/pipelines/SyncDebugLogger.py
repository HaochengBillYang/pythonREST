from asyncore import file_dispatcher
import time
from datetime import datetime

from request.Request import Request, Response, Pipeline, RestRequest
from utils.Logging import ColorCode


class SyncDebugLogger(Pipeline):
    def into_file(self, msg: str) -> None:
        file = open("/home/hcd/Documents/webserverlog.txt", "a")
        file.writelines(msg+"</br>")
        

    def __init__(self, logger_name: str):
        self.logger_name = logger_name

    def logger(self, color: ColorCode, message: str, with_time: bool = True) -> None:
        if with_time:
            now = datetime.now()
            date_time = now.strftime("%m/%d-%H:%M:%S]")
            print( color.to_code() + "[" + self.logger_name, date_time + message + ' ' +ColorCode.RESET.to_code())
            file_build =  color.to_html() + "[" + self.logger_name + ' ' + date_time + message + ColorCode.RESET.to_html()
            self.into_file(file_build)
        else:
            print( color.to_code() + message + ' ' + ColorCode.RESET.to_code())
            file_build = color.to_html() + message + ColorCode.RESET.to_html()
            self.into_file(file_build)

    def invoke_before_request(self, request: Request):
        console_build = "<============================================== timestamp=" + str(int(time.time() * 1000)) + " =>"
        print(console_build)
        file_build = "<============================================== timestamp=" + str(int(time.time() * 1000)) + " =>"
        self.into_file(file_build)
        method = "Form Post"
        if "RestRequest" in request.__class__.__name__:
            method = str(request.method)

        self.logger(ColorCode.BLUE, method + " " + request.url)
        for k in request.headers.keys():
            self.logger(ColorCode.YELLOW, k + ":" + request.headers[k], False)

        for k in request.data:
            self.logger(ColorCode.CYAN, k + " = " + str(request.data[k]), False)

    def invoke_after_request(self, request: Request, response: Response):
        color = ColorCode.GREEN
        if 300 <= response.return_code < 400:
            color = ColorCode.YELLOW
        elif response.return_code >= 400:
            color = ColorCode.RED

        self.logger(color, " << " + request.url + " ;code = " + str(response.return_code))
        self.logger(color, response.return_data, False)
        console_build = "<============================================== timestamp=" + str(int(time.time() * 1000)) + " => \n\n\n"
        print(console_build)
        file_build = "<============================================== timestamp=" + str(int(time.time() * 1000)) + " => </br>"
        self.into_file(file_build)
