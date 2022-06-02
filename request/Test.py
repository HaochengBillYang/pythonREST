import json
from typing import TypeVar

from operation.Operation import GetAllClustersOperation, GetAllClustersRequest

op = GetAllClustersOperation(
    host="https://172.16.4.248:8443"
).invoke(GetAllClustersRequest())
