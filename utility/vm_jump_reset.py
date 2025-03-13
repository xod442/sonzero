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


Usage: This python file reverts and resets all VM's and deletes all Distributed
Virtual switches

'''
from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
from utility.revert_vm import revert_vm
from utility.write_log import write_log
from utility.jump_list import jump_list
import ssl
import datetime
import logging

def vm_jump(jump_ip,j_user,j_password,jump_list,db):

    logging.basicConfig(filename="zero.log",
    					format='%(asctime)s %(message)s',
    					filemode='a')

    sslContext = ssl._create_unverified_context()

    port="443"

    # Create a connector to vsphere
    si = SmartConnect(
        host=jump_ip,
        user=j_user,
        pwd=j_password,
        port=port,
        sslContext=sslContext
    )

    content = si.RetrieveContent()

    vm_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.VirtualMachine],
                                                     True)
    vm_data = vm_list.view

    #---------------------------------------------------------------------------
    #
    #  Step 1: Revert & Reset VM's
    #
    #---------------------------------------------------------------------------
    counter = 0

    # reboot all student jump host vm's.
    for vm in vm_data:
        if vm.name in jump_list:

            # Power On the VM
            vm.ResetVM_Task()
            # Compose log information
            when = str(datetime.datetime.now())
            message = "%s ==> %s: has been rebooted" % (when, vm.name)
            logging.warning(message)
            response = write_log(db,message)
            counter = counter + 1



    vm_list.Destroy()
    when = str(datetime.datetime.now())
    message = "%s ==> All student jumphosts have been rebooted\n" % (when)
    logging.warning(message)
    response = write_log(db,message)

    return
