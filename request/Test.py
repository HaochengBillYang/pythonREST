import json

from pydantic import BaseModel

from request.Request import FormRequest
from request.pipelines.SimpleLogger import SimpleLogger

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


test = FormRequest("https://172.16.4.248:8443/oauth/token")


class Data(BaseModel):
    grant_type: str = "password"
    username: str
    password: str


class Response(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

data = Data(username="admin", password="Hello123!")

resp = test\
    .add_pipeline(SimpleLogger("Test"))\
    .add_header("Authorization", "Basic aGNkLWNsaWVudDpoY2Qtc2VjcmV0")\
    .set_data(data.dict())\
    .send()

des = Response(**(json.loads(resp.return_data)))

print(des.access_token)








