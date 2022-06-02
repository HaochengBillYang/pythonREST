from request.Request import FormRequest
from request.pipelines.SimpleLogger import SimpleLogger

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


test = FormRequest("https://172.16.4.248:8443/oauth/token")

resp = test\
    .add_pipeline(SimpleLogger("Test"))\
    .add_header("Authorization", "Basic aGNkLWNsaWVudDpoY2Qtc2VjcmV0")\
    .set_data({
        "grant_type": "password",
        "username": "admin",
        "password": "Hello123!"
    })\
    .send()
