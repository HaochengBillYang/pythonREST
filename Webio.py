import requests.exceptions
from pywebio.input import *
from pywebio.output import *
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


def out(operation, reply):      # Shows and logs the operation done
    log = {
        'operation_msg': 'Defined Operation: ' + str(operation),
        'request_msg': 'HTTP Request: ' + str(reply.request),
        'url_msg': 'URL: ' + str(reply.url),
        'result_msg': 'Result: ' + str(reply.json()),
    }
    for line, content in log.items():
        put_code(content)       # Each message get a code block in UI


def looper():                   # Function changes button_value by calling two buttons in UI
    return actions('Continue?', buttons=[{'label': 'New Instance', 'value': 1}, {'label': 'End', 'value': 0}])


def invalid_url():              # Throws invalid url error in UI
    put_error('Error: Invalid URL')


def static_bar(name: str, val: float):      # Sets a static bar of given name
    put_processbar(name)
    set_processbar(name, val)


def checkform(form):            # Checks for useless inputs in UI
    print(form)
    a = form['type']
    for i in range(len(all_functions)):
        if all_functions[i] not in a:
            if form[str(i)] != '':
                return str(i), 'Function not called, please remove input'


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

def get_everything_as_tree(link, portal, key):
    clusterlist = []
    res1 = get_all_clusters(link, portal, key)
    all_clusterid = get_all_cluster_id_from_response(res1)
    cluster_count = 0
    for clusterid in all_clusterid:
        clusterlist.append(Cluster(clusterid))
        res2 = get_hosts_by_cluster_id(link, portal, key, clusterid)
        all_hostid = get_all_host_id_from_response(res2)
        host_count = 0
        for hostid in all_hostid:
            clusterlist[cluster_count].hosts.append(Host(hostid))
            res3 = get_disks_by_host_id(link, portal, key, hostid)
            all_diskid = get_all_disk_id_from_response(res3)
            for diskid in all_diskid:
                clusterlist[cluster_count].hosts[host_count].append(
                    Disk(diskid))
            host_count += 1
        cluster_count += 1
    return clusterlist

def assign_all_tags_for_host(link, portal, key, id: str):
    pass

# Default value of button value, 1 is new instance and 0 is exit
button_value = 1
all_functions = ['Create Cluster', 'Create Vol.', 'Create Init.',
                 'Create Vol. Acc. Grp.', 'Login Vol.', 'Logout Vol.']      # Append as needed


while button_value:

    info = input_group("Operation Info", [
        input('Machine URL', name='url', placeholder='172.16.4.241', type=URL),
        input('Port', name='port', placeholder='8443'),
        input('URL Extension (if any)', name='ext',
              placeholder='/v1/clusters/'),
        input('Password', name='pwd', type=PASSWORD),
        checkbox('Operation Type', name='type', options=all_functions,
                 value=[i for i in range(len(all_functions))]),
        input('Create Cluster Name', name='0'),
        input('Create Volume Number', name='1'),
        input('Create Initiator Name', name='2'),
        input('Create Volume Access Group Name', name='3'),
        input('Login Volume Name', name='4'),
        input('Logout Volume Name', name='5')
    ], validate=checkform)

    type = info['type']
    port = info['port']
    url = info['url']
    ext = info['ext']

    if all_functions[0] in type:
        params = []                     # Request parameters
        try:                            # Add loop to continuous get data
            key = get_token(url, port)
            r = get_all_host(url, port, key)
            test_msg = get_all_host_id_from_response(r)
            out(type, r)              # Print Operation
            print(test_msg)
            button_value = looper()     # End Here
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()               # Print Error Message
            button_value = looper()     # End Here

    elif all_functions[1] in type:
        params = []
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[2] in type:
        params = []
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[3] in type:
        params = []
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[4] in type:
        params = []
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[5] in type:
        params = []
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    else:
        r = None
