'''
888888888888                                      88              88
         ,88                                      88              88
       ,88"                                       88              88
     ,88"     ,adPPYba,  8b,dPPYba,   ,adPPYba,   88  ,adPPYYba,  88,dPPYba,
   ,88"      a8P_____88  88P'   "Y8  a8"     "8a  88  ""     `Y8  88P'    "8a
 ,88"        8PP"""""""  88          8b       d8  88  ,adPPPPP88  88       d8
88"          "8b,   ,aa  88          "8a,   ,a8"  88  88,    ,88  88b,   ,a8"
888888888888  `"Ybbd8"'  88           `"YbbdP"'   88  `"8bbdP"Y8  8Y"Ybbd8"'

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0.

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "0.1.1"
__maintainer__ = "Rick Kauffman"
__status__ = "Alpha"


Usage: This python file processes a list of switches and executes a checkpoint rollback.

'''
from switch_list import switch_list
from pyaoscx.session import Session
from pyaoscx.configuration import Configuration
from pyaoscx.device import Device
from pyaoscx.pyaoscx_factory import PyaoscxFactory
import urllib3
from time import sleep
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys

switch_user = 'admin'
switch_password = 'admin'

    # from the utility/switch_list.py get a list of switches to reboot

version = '10.04'
# Set config names

# Open Session
switch = sys.argv[1]
s = Session(switch, version)
s.open(switch_user, switch_password)


device_obj = Device(s)
device_obj.boot_firmware()

when = str(datetime.datetime.now())
message = "%s ==> Switch: %s has has been rebooted\n" % (when, switch)
print(message)
#response = write_log(db,message)

# At the end, the session MUST be closed
s.close()
