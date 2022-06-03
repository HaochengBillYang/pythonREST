import json
from typing import TypeVar
import urllib3

from operation.disk.GetDisksByHostId import GetDisksByHostIdOperation, GetDisksByHostIdRequest
from operation.disk.GiveDiskTagById import GiveDiskTagByIdOperation, GiveDiskTagByIdRequest
from operation.disk.RemoveDiskTagById import RemoveDiskTagByIdOperation, RemoveDiskTagByIdRequest
from operation.host.GetAllHost import GetAllHostOperation, GetAllHostRequest
from operation.volume.CreateVolume import CreateVolumeOperation, CreateVolumeRequest

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from operation.Operation import *

op0 = CreateVolumeOperation(
    host="https://172.16.4.248:8443"
).invoke(CreateVolumeRequest(
    clusterId="60bf5cf5-e510-4960-8f53-b85396e03541",
    volumeName="test",
    volumeSize=10737418240,
    type="NORMAL"
))

op = GetAllHostOperation(
    host="https://172.16.4.248:8443"
).invoke(GetAllHostRequest(
    clusterId="60bf5cf5-e510-4960-8f53-b85396e03541"
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
