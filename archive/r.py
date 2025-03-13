from utility.switch_list import switch_list
from pyaoscx.session import Session
from pyaoscx.configuration import Configuration
from pyaoscx.device import Device
from pyaoscx.pyaoscx_factory import PyaoscxFactory
import urllib3
import datetime


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

version ='10.09'

switch='10.250.201.101'

switch_user = 'admin'
switch_password = 'admin'

for switch in switch_list:
    print(switch)
    s = Session(switch, version)
    s.open(switch_user, switch_password)
    config_obj = Configuration(s)
    reponse = config_obj.create_checkpoint('ZERO', 'startup-config')
    s.close()
