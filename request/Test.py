import json
from typing import TypeVar
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from operation.Operation import *

op = GetAllHostOperation(
    host="https://172.16.4.248:8443"
).invoke(GetAllHostRequest(
    onlyFreeHost=True
))

print(op.data)

op = GetDisksByHostIdOperation(
    host="https://172.16.4.248:8443"
).invoke(GetDisksByHostIdRequest(
    hostId=op.data[0].hostId
))

print(op.data)