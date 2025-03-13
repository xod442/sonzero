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
import ssl
import datetime
import logging
import time


def makepgrp(si):
    logging.basicConfig(filename="zero.log",
    					format='%(asctime)s %(message)s',
    					filemode='a')

    content = si.RetrieveContent()

    dvs_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.DistributedVirtualSwitch],
                                                     True)

    for dv_switch in dvs_list.view:
        if dv_switch.name == 'LG01-dvs-1':
            info = ['LG01-DP-01',10]
        if dv_switch.name == 'LG01-dvs-2':
            info = ['LG01-DP-02',20]

        if dv_switch.name == 'LG02-dvs-1':
            info = ['LG02-DP-01',10]
        if dv_switch.name == 'LG02-dvs-2':
            info = ['LG02-DP-02',20]

        if dv_switch.name == 'LG03-dvs-1':
            info = ['LG03-DP-01',10]
        if dv_switch.name == 'LG03-dvs-2':
            info = ['LG03-DP-02',20]

        if dv_switch.name == 'LG04-dvs-1':
            info = ['LG04-DP-01',10]
        if dv_switch.name == 'LG04-dvs-2':
            info = ['LG04-DP-02',20]

        if dv_switch.name == 'LG05-dvs-1':
            info = ['LG05-DP-01',10]
        if dv_switch.name == 'LG05-dvs-2':
            info = ['LG05-DP-02',20]

        if dv_switch.name == 'LG06-dvs-1':
            info = ['LG06-DP-01',10]
        if dv_switch.name == 'LG06-dvs-2':
            info = ['LG06-DP-02',20]

        if dv_switch.name == 'LG07-dvs-1':
            info = ['LG07-DP-01',10]
        if dv_switch.name == 'LG07-dvs-2':
            info = ['LG07-DP-02',20]

        if dv_switch.name == 'LG08-dvs-1':
            info = ['LG08-DP-01',10]
        if dv_switch.name == 'LG08-dvs-2':
            info = ['LG08-DP-02',20]

        if dv_switch.name == 'LG09-dvs-1':
            info = ['LG09-DP-01',10]
        if dv_switch.name == 'LG09-dvs-2':
            info = ['LG09-DP-02',20]

        if dv_switch.name == 'LG10-dvs-1':
            info = ['LG10-DP-01',10]
        if dv_switch.name == 'LG10-dvs-2':
            info = ['LG10-DP-02',20]

        response = add_dvPort_group(si, dv_switch, info)

    return response

def wait_for_task(task, actionName='job', hideResult=False):

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(5)

    if task.info.state == vim.TaskInfo.State.success:
        out = '%s Port group added to DVS.' % actionName
        logging.warning(out)
    else:
        out = '%s Port group is running long...no worries: %s' % (actionName, task.info.state)
        logging.warning(out)

    return task.info.result

def add_dvPort_group(si, dv_switch, info):

    dv_pg_spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
    dv_pg_spec.name = info[0]
    dv_pg_spec.numPorts = 8
    dv_pg_spec.type = vim.dvs.DistributedVirtualPortgroup.PortgroupType.earlyBinding
    dv_pg_spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
    dv_pg_spec.defaultPortConfig.securityPolicy = vim.dvs.VmwareDistributedVirtualSwitch.SecurityPolicy()

    vlan_spec = vim.dvs.VmwareDistributedVirtualSwitch.VlanIdSpec()
    vlan_spec.vlanId = info[1]
    dv_pg_spec.defaultPortConfig.vlan = vlan_spec

    dv_pg_spec.defaultPortConfig.securityPolicy.allowPromiscuous = vim.BoolPolicy(value=True)
    dv_pg_spec.defaultPortConfig.securityPolicy.forgedTransmits = vim.BoolPolicy(value=True)

    dv_pg_spec.defaultPortConfig.vlan.inherited = False
    dv_pg_spec.defaultPortConfig.securityPolicy.macChanges = vim.BoolPolicy(value=False)
    dv_pg_spec.defaultPortConfig.securityPolicy.inherited = False
    task = dv_switch.AddDVPortgroup_Task([dv_pg_spec])

    wait_for_task(task)

    return task.info.result
