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

op2 = GetDisksByHostIdOperation(
    host="https://172.16.4.248:8443"
).invoke(GetDisksByHostIdRequest(
    hostId=op.data[0].hostId
))

print(op2.data)


op3 = GiveDiskTagByIdOperation(
    host="https://172.16.4.248:8443"
).invoke(GiveDiskTagByIdRequest(
    hostId=op.data[0].hostId,
    diskIds=[op2.data[0].diskId],
    diskTag='DATA_DISK'
))


op4 = RemoveDiskTagByIdOperation(
    host="https://172.16.4.248:8443"
).invoke(RemoveDiskTagByIdRequest(
    hostId=op.data[0].hostId,
    diskIds=[op2.data[0].diskId],
    diskTag='DATA_DISK'
))


print(op4)
