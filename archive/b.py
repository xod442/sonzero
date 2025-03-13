
import ssl
from pyaoscx.session import Session
from pyaoscx.configuration import Configuration
from pyaoscx.pyaoscx_factory import PyaoscxFactory
from pyaoscx.vlan import Vlan
from pyaoscx.interface import Interface
import urllib3
from pyaoscx.device import Device
import datetime
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

switch_ip=["10.251.1.12"] # One 10K switch
version = "10.09"  #set version

switch_user = "admin"
switch_password = "admin"


    # Open Session
switch = str(switch_ip[0])
s = Session(switch, version)
s.open(switch_user, switch_password)

when = str(datetime.datetime.now())


device_obj = Device(s)
print(device_obj)
version = device_obj.get_firmware_version()
print(version)
s.close()
