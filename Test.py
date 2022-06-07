import json
from typing import TypeVar
import urllib3
#{%extends "base.html"%}
from operation.cluster.GetAllClusters import GetAllClustersOperation, GetAllClustersRequest
from operation.disk.GetDisksByHostId import GetDisksByHostIdOperation, GetDisksByHostIdRequest
from operation.disk.GiveDiskTagById import GiveDiskTagByIdOperation, GiveDiskTagByIdRequest
from operation.disk.RemoveDiskTagById import RemoveDiskTagByIdOperation, RemoveDiskTagByIdRequest
from operation.host.GetAllHost import GetAllHostOperation, GetAllHostRequest
from operation.task.TraceTask import TraceTaskOperation, TraceTaskRequest
from operation.task.TraceUntilComplete import TraceUntilCompleteOperation, TraceUntilCompleteRequest
from operation.volume.CreateVolume import CreateVolumeOperation, CreateVolumeRequest
from operation.volume.DeleteVolume import DeleteVolumeOperation, DeleteVolumeRequest
from webserver.op import generate_list_on_cluster

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from operation.Operation import *

op1 = GetAllClustersOperation(
    host="https://172.16.4.248:8443"
).invoke(GetAllClustersRequest(

))


print(generate_list_on_cluster("https://172.16.4.248","8443","d309fb6c-3115-4356-83d0-de23e9bc4071"))
