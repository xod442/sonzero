
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

switch_ip=["10.250.210.101","10.250.210.102"] # One 10K switch
version = "10.09"  #set version

switch_user = "admin"
switch_password = "admin"

for switch in switch_ip:
    print("starting loop")
    # Open Session
    switch = str(switch)
    s = Session(switch, version)
    s.open(switch_user, switch_password)
    device_obj = Device(s)
    device_obj.boot_firmware()
    s.close()
    print("sleeping20")
    time.sleep(20)
