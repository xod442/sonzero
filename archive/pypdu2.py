
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


#------------------------------------------------------------------------------
#
#                              PROCESS PDUs
#
#------------------------------------------------------------------------------

pdu_list = ['https://10.202.63.10']

username = 'arubatm'
password = 'Admin123!@#'

for pdu in pdu_list:

    ## Create a REDFISH object for PUD 1 R5025spdu01
    REDFISH_OBJ = redfish_client(base_url=pdu,
                                username=username,
                                password=password,
                                default_prefix='/redfish/v1')

    REDFISH_OBJ.login

    port_list = [7]
    outlet_list = ['OUTLET7']
    outlet_name_list = ['OUTLETSeven']

    array_position = 0

    for port in port_list:
        # Set HTTP POST to turn off port
        body = {
        "OutletNumber": port,
        "StartupState":"off",
        "OutletName": outlet_name_list[array_position],
        "OnDelay": 5,
        "OffDelay": 6,
        "RebootDelay": 7,
        "OutletStatus": "off"
        }
        print(body)
        # Turn port off
        url = "/redfish/v1/PowerEquipment/RackPDUs/1/Outlets/"+outlet_list[array_position]+"/Outlet.PowerControl"
        print(url)
        print('port %s off' % port)
        response = REDFISH_OBJ.post(url, body=body)
        print(response.status)
        # pprint(dir(response))

        if response.text:
            print('Response from port toggle %s ====>' % pdu)
            #response = json.loads(response)
            pprint(response)
            print(type(response))
        else:
            print('Nothing Returned')
        # Set HTTP POST to turn on port
        body = {
        "OutletNumber": port,
        "StartupState":"on",
        "OutletName": outlet_name_list[array_position],
        "OnDelay": 5,
        "OffDelay": 6,
        "RebootDelay": 7,
        "OutletStatus": "on"
        }
        print(body)
        # Turn port on
        print('port %s on' % port)
        response = REDFISH_OBJ.post(url, body=body)
        print(response.status)
        if response.text:
            print('Response from port toggle %s ====>' % pdu)
            # response = json.loads(response)
            pprint(response)
            print(type(response))
        else:
            print('Nothing Returned')

        array_position = array_position + 1

    REDFISH_OBJ.logout
