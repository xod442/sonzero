import concurrent.futures
import urllib.request

from utility.boot_switch import boot_switch
from pyaoscx.session import Session
from pyaoscx.configuration import Configuration
from pyaoscx.pyaoscx_factory import PyaoscxFactory
from pyaoscx.vlan import Vlan
from pyaoscx.interface import Interface
import urllib3
from pyaoscx.device import Device
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


ips = ['10.251.1.11',
        '10.251.1.12',
        '10.251.1.13',
        '10.251.1.14',
        '10.251.1.15']

version = '10.04'
switch_user = 'admin'
switch_password = 'admin'


for ip in ips:
    print("IP: %s, Version: %s, User: %s, Password: %s" % (ip,version,switch_user,switch_password))
    #myTypeIp = type(ip)
    print("This is the type: The IP address is %s" % (ip))
    print("This is the version type: The IP address is %s" % (ip))
    print("This is the user: The IP address is %s" % (ip))
    print("This is the password: The IP address is %s" % (ip))
