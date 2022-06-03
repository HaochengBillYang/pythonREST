import requests.exceptions
import requests as req


def get_all_clusters(link, portal, key):
    tmp = req.get(url=link + ":" + portal + "/v1/clusters",
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
    tmp = req.get(url=link + ":" + portal + "/v1/hosts",
                  data=id_param,
                  headers={"Authorization": "bearer" + str(key)}, verify=False)
    return tmp


def get_disks_by_host_id(link, portal, key, id: str):
    tmp = req.get(url=link + ":" + portal + "/v1/disks/by-host/" + id,
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
