import requests
import socket
import getmac

import Modules.exceptions as Exceptions 

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