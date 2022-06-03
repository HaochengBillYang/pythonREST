from pip import main
from operation.Operation import *


#
# Deprecated Warning
# This file was used for Compatibility
# Should refer to /operation/Operation.py
#
from operation.cluster.GetAllClusters import GetAllClustersOperation, GetAllClustersRequest
from operation.disk.GetDisksByHostId import GetDisksByHostIdOperation, GetDisksByHostIdRequest
from operation.disk.GiveDiskTagById import GiveDiskTagByIdOperation, GiveDiskTagByIdRequest
from operation.disk.RemoveDiskTagById import RemoveDiskTagByIdRequest, RemoveDiskTagByIdOperation
from operation.host.GetAllHost import GetAllHostOperation, GetAllHostRequest


class DummyResponse:
    def __init__(self, ok: bool, content: str):
        self.ok: bool = ok
        self.content: str = content

    def json(self):
        return self.content


def give_disk_tag_by_id(link, port, disk: list, tag) -> DummyResponse:
    try:
        op = GiveDiskTagByIdOperation(
            host=link + ":" + str(port)
        ).invoke(GiveDiskTagByIdRequest(
            hostId=disk[1],
            diskIds=[disk[0]],
            diskTag=tag
        ))
        return DummyResponse(True, str(op))
    except Exception as e:
        return DummyResponse(False, str(e))


def remove_datadisk_tag_by_id(link, port, disk, tag) -> DummyResponse:
    try:
        op = RemoveDiskTagByIdOperation(
            host=link + ":" + str(port)
        ).invoke(RemoveDiskTagByIdRequest(
            hostId=disk[1],
            diskIds=[disk[0]],
            diskTag=tag
        ))
        return DummyResponse(True, str(op))
    except Exception as e:
        return DummyResponse(False, str(e))


def generate_list(link, port):
    main_list = []
    server_host = link + ":" + str(port)

    for cluster in GetAllClustersOperation(server_host).invoke(GetAllClustersRequest()).data:
        for host in GetAllHostOperation(server_host).invoke(GetAllHostRequest(clusterId=cluster.clusterId)).data:
            for disk in GetDisksByHostIdOperation(server_host).invoke(GetDisksByHostIdRequest(hostId=host.hostId)).data:
                main_list.append({
                    disk.diskId,
                    host.hostId,
                    cluster.clusterId
                })

    print("successfully returned")
    print(main_list)
    return main_list
