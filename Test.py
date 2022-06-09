import json
from typing import TypeVar
import urllib3
# {%extends "base.html"%}
from config.Config import ConnectionConfig, HostConfig
from config.ConfigManagement import save_config, retrieve_config_by_type, remove_config_by_id
from operation.cluster.CreateCluster import CreateClusterOperation, CreateClusterRequest, CreateClusterInfo
from operation.cluster.GetAllClusters import GetAllClustersOperation, GetAllClustersRequest
from operation.disk.GetDisksByHostId import GetDisksByHostIdOperation, GetDisksByHostIdRequest
from operation.disk.GiveDiskTagById import GiveDiskTagByIdOperation, GiveDiskTagByIdRequest
from operation.disk.RemoveDiskTagById import RemoveDiskTagByIdOperation, RemoveDiskTagByIdRequest
from operation.host.GetAllHost import GetAllHostOperation, GetAllHostRequest
from operation.host.HostJoinCluster import HostJoinClusterOperation, HostJoinClusterRequest
from operation.task.TraceTask import TraceTaskOperation, TraceTaskRequest
from operation.task.TraceUntilComplete import TraceUntilCompleteOperation, TraceUntilCompleteRequest
from operation.volume.CreateVolume import CreateVolumeOperation, CreateVolumeRequest
from operation.volume.DeleteVolume import DeleteVolumeOperation, DeleteVolumeRequest
from webserver.op import generate_list_on_cluster, generate_list_on_cluster_to_str

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for host in GetAllHostOperation("https://172.16.4.248:8443").invoke(
        GetAllHostRequest(

        )
).data:

    if "53" not in host.hostName:
        print("Join {0} ({1} )".format(host.hostId, host.hostName))
        HostJoinClusterOperation("https://172.16.4.248:8443").invoke(
            HostJoinClusterRequest(
                clusterId="1d1c7573-ae13-4200-9058-a6c0929ac08f",
                hosts=[host.hostId]
            )
        )
