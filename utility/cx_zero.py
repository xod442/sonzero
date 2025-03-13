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
from utility.switch_list import switch_list
from utility.write_log import write_log
from pyaoscx.session import Session
from pyaoscx.configuration import Configuration
from pyaoscx.device import Device
from pyaoscx.pyaoscx_factory import PyaoscxFactory
import urllib3
import datetime
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def cx_zero(db):

    logging.basicConfig(filename="zero.log",
    					format='%(asctime)s %(message)s',
    					filemode='a')

    # from the utility/switch_list.py get a list of switches to rollback to zero

    version = '10.04'

    top = 0
    bot = 0
    for switch in switch_list:
        try:
            s = Session(switch, version)
            s.open(db['switch_user'], db['switch_password'])
            config_obj = Configuration(s)
            reponse = config_obj.create_checkpoint('ZERO', 'startup-config')
            print('rollback %s' % switch)
            s.close()
            message = 'Top Loop-Trip - %s____Set rollback to startup-config %s' % (top,switch)
            logging.warning(message)
        except:
            message = 'Top ALERT!!!!!!!!!-Trip - %s_____Failed to ZERO to startup-config %s' % (top,switch)
            logging.warning(message)
        top = top + 1

    for switch in switch_list:

        try:
            s = Session(switch, version)
            s.open(db['switch_user'], db['switch_password'])
            config_obj = Configuration(s)
            reponse = config_obj.create_checkpoint('ZERO', 'running-config')
            print('rollback %s' % switch)
            s.close()
            message = 'Bottom Loop-Trip - %s____Set rollback to running-config %s' % (bot,switch)
            logging.warning(message)
        except:
            message = 'Bottom ALERT!!!!!!!!!-Trip - %s_____Failed to ZERO to running-config %s' % (bot,switch)
            logging.warning(message)
        bot = bot + 1

    when = str(datetime.datetime.now())
    message = '==================== ALL SWITCHES ARE ZERO ===================='
    logging.warning(message)
    return
