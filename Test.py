import json
from typing import TypeVar
import urllib3

from operation.cluster.GetAllClusters import GetAllClustersOperation, GetAllClustersRequest
from operation.disk.GetDisksByHostId import GetDisksByHostIdOperation, GetDisksByHostIdRequest
from operation.disk.GiveDiskTagById import GiveDiskTagByIdOperation, GiveDiskTagByIdRequest
from operation.disk.RemoveDiskTagById import RemoveDiskTagByIdOperation, RemoveDiskTagByIdRequest
from operation.host.GetAllHost import GetAllHostOperation, GetAllHostRequest
from operation.task.TraceTask import TraceTaskOperation, TraceTaskRequest
from operation.task.TraceUntilComplete import TraceUntilCompleteOperation, TraceUntilCompleteRequest
from operation.volume.CreateVolume import CreateVolumeOperation, CreateVolumeRequest
from operation.volume.DeleteVolume import DeleteVolumeOperation, DeleteVolumeRequest

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from operation.Operation import *

op1 = GetAllClustersOperation(
    host="https://172.16.4.248:8443"
).invoke(GetAllClustersRequest(

))

op2 = CreateVolumeOperation(
    host="https://172.16.4.248:8443"
).invoke(CreateVolumeRequest(
    clusterId=op1.data[0].clusterId,
    volumeName="test",
    volumeSize=1073741824,
))

op3 = DeleteVolumeOperation(
    host="https://172.16.4.248:8443"
).invoke(DeleteVolumeRequest(
    clusterId=op1.data[0].clusterId,
    byName=True,
    volumeIdOrNameList=["test"],
    force=False
))

op4 = TraceUntilCompleteOperation(
    host="https://172.16.4.248:8443"
).invoke(TraceUntilCompleteRequest(
    taskId=op3.taskId
))
