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


ips = ['10.251.1.13',
        '10.251.1.12',
        '10.251.1.11']

version = '10.04'
switch_user = 'admin'
switch_password = 'admin'


# Retrieve a single page and report the URL and contents
def process_ip(ip,version,switch_user,switch_password):
    try:
        s = Session(ip, version)
        s.open(switch_user, switch_password)
        # Now reboot the switch
        print("booting %s" % (ip))
        device_obj = Device(s)
        boot = device_obj.boot_firmware()
        time.sleep(2)
        print("post boot for switch: %s" (ip))
        s.close()
    except:
        print("blah---%s" % (ip))


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
    # Start the load operations and mark each future with its URL
    future_to_ip = {executor.submit(process_ip, ip, version, switch_user, switch_password): ip for ip in ips}
