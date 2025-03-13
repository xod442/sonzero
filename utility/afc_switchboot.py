#!/usr/bin/env python3
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


Usage: This python file reboots all switches by leveraging the AFC controller.

'''
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import requests
import os
import sys
import logging
import json
import pyafc.session as session
import pyafc.devices as devices
import pyafc.fabric as fabric
import pyafc.vsx as vsx
import pyafc.vrfs as vrfs
import pyafc.ntp as ntp
import pyafc.dns as dns
from utility.afc_ip import afc_ip
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)


def afc_switchboot(afc_user, afc_password, db):


    for ip in afc_ip:
        auth_header = {}
        switch_uuid_list = []
        base_url = "https://{0}/api/v1/".format(ip)

        try:
            login_session, auth_header = session.login(base_url, afc_user, afc_password)

            session_dict = dict(s=login_session, url=base_url)
            # Get a list of switches from the AFC

            switches = devices.get_all_switches(auth_header, **session_dict)
            if switches:
                for switch in switches:

                    uuid = switch['uuid']
                    switch_uuid_list.append(uuid)

                # Send the API
                print('sending request for %s' % switch_uuid_list)
                response = devices.reboot_switches(switch_uuid_list, auth_header, **session_dict)


            session.logout(auth_header, **session_dict)

        except Exception as error:
            print('Ran into exception creating switch dictionary: {}. Logging out...'.format(error))
            session.logout(auth_header, **session_dict)
    return












if __name__ == '__main__':
	main()
