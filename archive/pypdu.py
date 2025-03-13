
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

A redfish python script to access the API on the HPE G2 PDU (P9S15A)

'''
import sys
import json
from redfish import redfish_client
from redfish.rest.v1 import ServerDownOrUnreachableError
import requests
import redfish
from pprint import pprint

headers = {}
pdu_ip1 = 'https://10.202.63.10'
pdu_ip2 = 'https://10.202.63.12'

username = 'arubatm'
password = 'Admin123!@#'


## Create a REDFISH object for PUD 1 R5025spdu01
REDFISH_OBJ1 = redfish_client(base_url=pdu_ip1,
                            username=username,
                            password=password,
                            default_prefix='/redfish/v1')

REDFISH_OBJ1.login(auth='basic')

response = REDFISH_OBJ1.get("/redfish/v1/PowerEquipment/RackPDUs/1/OutletGroups", None)

if response.text:
    print('Response from R5025spud01 ====>')
    response = json.loads(response.text)
    pprint(response['SerialNumber'])
    print(type(response))
else:
    print('Nothing Returned')


## Create a REDFISH object for PUD 2 R5024spdu02
REDFISH_OBJ2 = redfish_client(base_url=pdu_ip2,
                            username=username,
                            password=password,
                            default_prefix='/redfish/v1')

REDFISH_OBJ2.login(auth='basic')

response = REDFISH_OBJ2.get("/redfish/v1/PowerEquipment/RackPDUs/1/OutletGroups", None)

#sys.stdout.write("%s\n" % response.text)
if response.text:
    print('Response from R5024spud01 ====>')
    response = json.loads(response.text)
    pprint(response['SerialNumber'])
    print(type(response))
else:
    print('Nothing Returned')



REDFISH_OBJ1.logout
REDFISH_OBJ2.logout
