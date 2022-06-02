import json
from typing import TypeVar
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from operation.Operation import GetAllClustersOperation, GetAllClustersRequest

op = GetAllClustersOperation(
    host="https://172.16.4.248:8443"
).invoke(GetAllClustersRequest())

print(op.data)
