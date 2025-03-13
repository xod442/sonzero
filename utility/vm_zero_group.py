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
import ssl
import datetime
import logging

def traverse_snapshots(snapshot_tree):
    # Recursively traverse and collect all snapshots
    snapshots = []
    for child_snapshot in snapshot_tree:
        snapshots.append(child_snapshot)
        snapshots.extend(traverse_snapshots(child_snapshot.childSnapshotList))
    return snapshots

def vm_zero_group(vsphere_ip,vsphere_user,vsphere_pass,lab_vm_names,dvs_name,level):

    logging.basicConfig(filename="zero.log",
    					format='%(asctime)s %(message)s',
    					filemode='a')

    sslContext = ssl._create_unverified_context()

    port="443"

    # Create a connector to vsphere
    si = SmartConnect(
        host=vsphere_ip,
        user=vsphere_user,
        pwd=vsphere_pass,
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

    # revert all vms to snapshot named INITIAL and reboot or reset vm.
    counter = 0
    for vm in vm_data:
        if vm.name in lab_vm_names:
            if vm.snapshot:
                snapshot_tree = vm.snapshot.rootSnapshotList
                snapshot_list = traverse_snapshots(snapshot_tree)
                if snapshot_list:
                    for snapshot in snapshot_list:

                        if snapshot.name == level:
                            when = str(datetime.datetime.now())
                            # Power Off the VM
                            vm.PowerOff()
                            message = "%s ==> vm%s: %s has been powered OFF\n" % (counter,when,vm.name)
                            logging.warning(message)
                            response = write_log(db,message)
                            # Revert VM
                            response = revert_vm(snapshot.snapshot)
                            # Power On the VM
                            vm.ResetVM_Task()
                            # Compose log information
                            when = str(datetime.datetime.now())
                            message = "%s ==> vm%s: %s has been reverted and powered back ON\n" % (counter,when,vm.name)
                            logging.warning(message)
                            response = write_log(db,message)
                            counter = counter + 1



    vm_list.Destroy()


    #---------------------------------------------------------------------------
    #
    #  Step 2: Delete the distributed virtual switches created in HOL
    #
    #      D A N G E R    W I L L R O B I N S O N ! ! ! ! ! ! !
    #      This will violently destroy every distributed Virtual Switch
    #---------------------------------------------------------------------------

    dvs_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.DistributedVirtualSwitch],
                                                     True)

    for dvs in dvs_list.view:
        if dvs.name == dvs_name:
            task = dvs.Destroy_Task()
            response = WaitForTask(task)
    dvs_list.Destroy()

    # si.Disconnect()

    when = str(datetime.datetime.now())
    message = "%s ==> The distributed virtual switch has been removed\n" % (when)
    logging.warning(message)

    return
