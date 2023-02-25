from datetime import datetime
import requests
import socket
import getmac
import os

import Modules.exceptions as Exceptions 
import Modules.display as Display

def net_info(args):
    """ Show network information. (PCname, Public and Private IP, MAC)"""
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=3).text
    except requests.exceptions.ConnectTimeout:
        public_ip = "error"
    
    private_ip = socket.gethostbyname(socket.gethostname())
    pc_name = socket.gethostname()
    mac_address = getmac.get_mac_address()

    print(f"PC NAME: {pc_name}")
    print(f"Public IP: {public_ip}")
    print(f"Private IP: {private_ip}")
    print(f"MAC address: {mac_address}")

def dns_lookup(args):
    """ Get ip from address. """
    target_address = args['addr']

    try:
        target_ip = socket.gethostbyname(target_address)
        print(f"{target_address} = {target_ip}")
    except:
        raise Exceptions.CannotGatherInfo

def ip_lookup(args):
    """ Get address from ip. """
    target_ip = args['ip']

    try:
        target_address = socket.gethostbyaddr(target_ip)[0]
        print(f"{target_ip} = {target_address}")
    except:
        raise Exceptions.CannotGatherInfo

def ip_geo_info(args):
    """ Get ip's country and city informations. """
    target_ip = args['target']
    if target_ip == "":
        target_ip = "localhost"

    try:
        response = requests.get(f"http://ip-api.com/json/{target_ip}", timeout=3).json()
    except requests.exceptions.ConnectTimeout:
        raise Exceptions.CannotGatherInfo

    if response['status'] == 'fail':
        raise Exceptions.InvalidAddress

    print(f"Country: {response['country']} [{response['countryCode']}]")
    print(f"City: {response['city']} [{response['zip']}]")

def make_request(args):
    url = args['url']
    request_type = args['type'].lower()
    to_file = args['to_file']

    request_types = {
        "get": requests.get,
        "post": requests.post,
        "patch": requests.patch,
        "put": requests.put,
        "head": requests.head,
        "delete": requests.delete,
    }

    if request_type not in request_types:
        raise Exceptions.InvalidValue

    request = request_types[request_type]

    try:
        response = request(url, timeout=10)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        raise Exceptions.CannotConnect
    except requests.exceptions.MissingSchema:
        raise Exceptions.InvalidAddress
    except:
        raise Exceptions.CannotGatherInfo
    
    if response.status_code in range(200, 300):
        Display.Message.success(f"Status code: {response.status_code}")
    elif response.status_code in range(300, 400):
        Display.Message.warning(f"Status code: {response.status_code}")
    elif response.status_code in range(400, 600):
        Display.Message.error(f"Status code: {response.status_code}")
    else:
        Display.Message.info(f"Status code: {response.status_code}")
    
    content = response.text
    
    if to_file:
        current_time = datetime.now().strftime("%H_%M_%S")
        file_path = f".\\response {current_time}.txt"
        try:
            with open(file_path, "a+") as file:
                file.write(content)
            Display.Message.success(f"Response has been saved to: {os.path.abspath(file_path)}")

        except:
            print(f"Response:\n{content}")
            Display.Message.error(f"Response could not be saved to file: {os.path.abspath(file_path)}")

    else:
        print(f"Response:\n{content}")
    
