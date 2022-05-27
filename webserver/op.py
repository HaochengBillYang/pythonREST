import requests.exceptions
import requests as req


class Cluster:
    def __init__(self, id):
        self.id = id
        self.hosts = []
        self.attributes = {}


class Host:
    def __init__(self, id):
        self.id = id
        self.disks = []
        self.attributes = {}


class Disk:
    def __init__(self, id):
        self.id = id
        self.attributes = {}


def get_token(link, portal):    # Gets token on one call
    token_data = {'grant_type': 'password',
                  'username': 'admin', 'password': 'Hello123!'}
    token_header = {'Content-Type': 'application/x-www-form-urlencoded'}
    token = req.post(url=link+':'+portal+'/oauth/token', data=token_data, headers=token_header, auth=(
        'hcd-client', 'hcd-secret'), verify=False)  # data: form in insomnia, auth: HTTPbasic ('user', 'password')
    return token.json()['access_token']


def get_all_clusters(link, portal, key):
    tmp = req.get(url=link+':'+portal+'/v1/clusters',
                  headers={'Authorization': 'bearer' + str(key)}, verify=False)
    return tmp


def get_all_cluster_id_from_response(res: req.Response):
    ans = []
    for label, content in res.json().items():
        if label == 'data':
            for cluster_info in content:
                for a, b in cluster_info.items():
                    if a == 'clusterId':
                        ans.append(str(b))
    return ans


def get_cluster_by_id(link, portal, key, id: str):
    tmp = req.get(url=link+':'+portal+'/v1/clusters'+'/'+id,
                  headers={'Authorization': 'bearer' + str(key)}, verify=False)
    return tmp


def get_all_host(link, portal, key):
    tmp = req.get(url=link+':'+portal+'/v1/hosts',
                  headers={'Authorization': 'bearer' + str(key)}, verify=False)
    return tmp


def get_all_free_hosts(link, portal, key):
    free_param = {'onlyFreeHost': 'true'}
    tmp = req.get(url=link+':'+portal+'/v1/hosts', data=free_param,
                  headers={'Authorization': 'bearer' + str(key)}, verify=False)
    return tmp


def get_hosts_by_cluster_id(link, portal, key, id: str):
    id_param = {'clusterId': id}
    tmp = req.get(url=link+':'+portal+'/v1/hosts',
                  data=id_param,
                  headers={'Authorization': 'bearer' + str(key)}, verify=False)
    return tmp


def get_disks_by_host_id(link, portal, key, id: str):
    tmp = req.get(url=link+':'+portal+'/v1/disks/by-host/'+id,
                  headers={'Authorization': 'bearer' + str(key)}, verify=False)
    return tmp


def get_all_host_id_from_response(res: req.Response):
    ans = []
    for label, content in res.json().items():
        if label == 'data':
            for host_info in content:
                for a, b in host_info.items():
                    if a == 'hostId':
                        ans.append(str(b))
    return ans


def get_all_disk_id_from_response(res: req.Response):
    ans = []
    for label, content in res.json().items():
        if label == 'data':
            for disk_info in content:
                for a, b in disk_info.items():
                    if a == 'diskId':
                        ans.append(str(b))
    return ans


def get_all_attributes_from_response(res: req.Response):
    attr = {}
    for label, content in res.json().items():
        if label == 'data':
            for any_info in content:
                for a, b in any_info.items():
                    attr[a] = b
    return attr
