
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

'''
# -*- coding: utf-8 -*-
"""
An example of gathering the computer system details
"""
from redfish import redfish_client

# Set the Redfish API endpoint URL
redfish_url = 'https://10.202.63.10/redfish/v1'
username = 'arubatm'
password = 'Admin123!@#'

# Create a Redfish client instance
try:
    ## Create a REDFISH object
    client = redfish_client(base_url=redfish_url,
                               username=username,
                               password=password,
                               default_prefix='/redfish/v1')
except ServerDownOrUnreachableError as excp:
    sys.stderr.write('Server Unreachable or down.\n')
    sys.exit


try:
    # Connect to the Redfish service
    client.login()

    # Fetch the root service
    root_service = client.root

    print(root_service)

finally:
    # Logout and close the client connection
    client.logout()
