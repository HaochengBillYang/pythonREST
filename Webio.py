import requests.exceptions
from pywebio.input import *
from pywebio.output import *
import requests as req



def out(operation, reply):    # Shows and logs the operation done
    log = {
        'operation_msg': 'Defined Operation: ' + str(operation),
        'request_msg': 'HTTP Request: ' + str(reply.request), 
        'url_msg': 'URL: ' + str(reply.url),
        'result_msg': 'Result: ' + str(reply.json()),
    }
    for line,content in log.items():
        put_code(content)


def looper():       # Function changes button_value by calling two buttons
    return actions('Continue?', buttons=[{'label': 'New Instance', 'value': 1}, {'label': 'End', 'value': 0}])


def invalid_url():  # Throws invalid url error
    put_error('Error: Invalid URL')


def static_bar(name: str, val: float):   # Sets a static bar of given name
    put_processbar(name)
    set_processbar(name, val)


def checkform(form):
    print(form)
    a = form['type']
    for i in range(len(all_functions)):
        if all_functions[i] not in a:
            if form[str(i)] != '':
                return str(i), 'Function not called, please remove input'


def get_token(link, portal):
    token_data = {'grant_type': 'password', 'username': 'admin', 'password': 'Hello123!'}
    token_header = {'Content-Type': 'application/x-www-form-urlencoded'}
    token = req.post(url=link+':'+portal+'/oauth/token', data=token_data, headers=token_header, auth=('hcd-client','hcd-secret'), verify=False) #Unfinished
    return token.json()['access_token']

button_value = 1        # Default value of button value, 1 is new instance and 0 is exit with code 0
all_functions = ['Create Cluster', 'Create Vol.', 'Create Init.', 'Create Vol. Acc. Grp.', 'Login Vol.', 'Logout Vol.']


while button_value:

    info = input_group("Operation Info", [
        input('Machine URL', name='url', placeholder='172.16.4.241', type=URL),
        input('Port', name='port', placeholder='8443'),
        input('URL Extension (if any)', name='ext', placeholder='/v1/clusters/'),
        input('Password', name='pwd', type=PASSWORD),
        checkbox('Operation Type', name='type', options=all_functions, value=[i for i in range(len(all_functions))]),
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
        params = []     # Request parameters
        try:    # Add loop to continuous get data
            key = get_token(url, port)
            r = req.get(url=url+':'+port+ext, data=params, headers={'Authorization': 'bearer'+ str(key), 'Content-Type': 'application/json'}, verify=False)
            out(type, r)              # Print Operation
            button_value = looper()     # End Here
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()               # Print Error Message
            button_value = looper()     # End Here

    elif all_functions[1] in type:
        params=[]
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[2] in type:
        params=[]
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[3] in type:
        params=[]
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[4] in type:
        params=[]
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[5] in type:
        params=[]
        try:
            r = req.get(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    else:
        r = None







