import time
import requests.exceptions
from pywebio.input import *
from pywebio.output import *
import requests as req


def out(operation, request):    # Shows the operation done
    output_msg = 'Defined Operation: ' + str(type) + '\nHTTP Request: ' + str(url) + '\nRequested'
    put_code(output_msg)


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


button_value = 1        # Default value of button value, 1 is new instance and 0 is exit with code 0
all_functions = ['Create Cluster', 'Create Vol.', 'Create Init.', 'Create Vol. Acc. Grp.', 'Login Vol.', 'Logout Vol.']


while button_value:

    info = input_group("Operation Info", [
        input('Machine URL', name='url', placeholder='192.168.1.1', type=URL),
        input('Port', name='port', placeholder='8080'),
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

    put_code('Target Cluster:'+str(url))

    if all_functions[1] in type:
        params = []     # Request parameters
        try:    # Add loop to continuous get data
            r = req.get(url=url, data=params)
            value = 0.85                # Use parsed return: value = r.text
            static_bar('upload', value)     # Create static bar of given value
            out(type, url)              # Print Operation
            button_value = looper()     # End Here
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()               # Print Error Message
            button_value = looper()     # End Here

    elif all_functions[2] in type:
        params=[]
        try:
            r = req.delete(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[3] in type:
        params=[]
        try:
            r = req.post(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    elif all_functions[4] in type:
        params=[]
        try:
            r = req.put(url=url, data=params)
        except requests.exceptions.MissingSchema:       # Invalid URL will throw this exception
            invalid_url()  # Print Error Message
            button_value = looper()  # End Here
    else:
        r = None







