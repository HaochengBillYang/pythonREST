from pip import main
import requests.exceptions
import requests as req
from operation.Operation import *

#
# Deprecated Warning
# This file was used for Compatibility
# Should refer to /operation/Operation.py
#

def get_all_clusters(link, portal, key):
    tmp = req.get(url=link+":"+portal+"/v1/clusters",
                  headers={"Authorization": "bearer" + str(key)}, verify=False)
    return tmp


def get_all_cluster_id_from_response(res: req.Response):
    ans = []
    for label, content in res.json().items():
        if label == "data":
            for cluster_info in content:
                for a, b in cluster_info.items():
                    if a == "clusterId":
                        ans.append(str(b))
    return ans


def get_hosts_by_cluster_id(link, portal, key, id: str):
    id_param = {"clusterId": id}
    tmp = req.get(url=link+":"+portal+"/v1/hosts",
                  data=id_param,
                  headers={"Authorization": "bearer" + str(key)}, verify=False)
    return tmp

def get_disks_by_host_id(link, portal, key, id: str):
    tmp = req.get(url=link+":"+portal+"/v1/disks/by-host/"+id,
                  headers={"Authorization": "bearer" + str(key)}, verify=False)
    return tmp


def get_all_host_id_from_response(res: req.Response):
    ans = []
    for label, content in res.json().items():
        if label == "data":
            for host_info in content:
                for a, b in host_info.items():
                    if a == "hostId":
                        ans.append(str(b))
    return ans


def get_all_disk_id_from_response(res: req.Response):
    ans = []
    for label, content in res.json().items():
        if label == "data":
            for disk_info in content:
                for a, b in disk_info.items():
                    if a == "diskId":
                        ans.append(str(b))
    return ans


class DummyResponse:
    def __init__(self, ok:bool, content:str):
        self.ok:bool = ok
        self.content:str = content

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
                main_list.append([
                    disk.diskId,
                    host.hostId,
                    cluster.clusterId
                ])

    return main_list

def generate_list_old(link, portal, key):
    main_list = []
    ask1 = get_all_clusters(link, portal, key)
    clusters = get_all_cluster_id_from_response(ask1)
    for cluster in clusters:
        ask2 = get_hosts_by_cluster_id(link, portal, key, cluster)
        hosts = get_all_host_id_from_response(ask2)
        for host in hosts:
            ask3 = get_disks_by_host_id(link, portal, key, host)
            disks = get_all_disk_id_from_response(ask3)
            for disk in disks:
                main_list.append([disk, host, cluster])
    return main_list

