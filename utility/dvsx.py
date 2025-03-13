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


def makedvs(si, dv_switch_info):
    logging.basicConfig(filename="zero.log",
    					format='%(asctime)s %(message)s',
    					filemode='a')

    datacenter_name = 'DCN-ILT-VLAB'
    content = si.RetrieveContent()
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
    cluster = get_obj(content, [vim.ClusterComputeResource], dv_switch_info['cluster_id'])
    network_folder = datacenter.networkFolder
    #Create DV Switch
    dv_switch = create_dvSwitch(si, content, network_folder, cluster, dv_switch_info)

    return dv_switch

def get_obj(content, vimtype, name=None):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def wait_for_task(task, name, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(5)

    if task.info.state == vim.TaskInfo.State.success:
        out = '%s completed successfully...' % actionName
        logging.warning(out)
    else:
        out = '%s has not completed yet: %s' % (actionName, task.info.state)
        logging.warning(out)

    return task.info.result


def create_dvSwitch(si, content, network_folder, cluster, dv_switch_info):

    pnic_specs = []
    dvs_host_configs = []
    uplink_port_names = []
    dvs_create_spec = vim.DistributedVirtualSwitch.CreateSpec()
    dvs_config_spec = vim.DistributedVirtualSwitch.ConfigSpec()
    dvs_config_spec.name = dv_switch_info['dvs_name']
    dvs_config_spec.uplinkPortPolicy = vim.DistributedVirtualSwitch.NameArrayUplinkPortPolicy()
    hosts = cluster.host

    for x in range(len(hosts)):
        uplink_port_names.append("dvUplink%d" % x)

    for host in hosts:
        dvs_config_spec.uplinkPortPolicy.uplinkPortName = uplink_port_names
        dvs_config_spec.maxPorts = 9
        pnic_spec = vim.dvs.HostMember.PnicSpec()
        pnic_spec.pnicDevice = dv_switch_info['vnic']
        pnic_specs.append(pnic_spec)
        dvs_host_config = vim.dvs.HostMember.ConfigSpec()
        dvs_host_config.operation = vim.ConfigSpecOperation.add
        dvs_host_config.host = host
        dvs_host_configs.append(dvs_host_config)
        dvs_host_config.backing = vim.dvs.HostMember.PnicBacking()
        dvs_host_config.backing.pnicSpec = pnic_specs
        dvs_config_spec.host = dvs_host_configs

    dvs_create_spec.configSpec = dvs_config_spec
    dvs_create_spec.productInfo = vim.dvs.ProductSpec(version='7.0.2')

    task = network_folder.CreateDVS_Task(dvs_create_spec)

    response = wait_for_task(task, si, dv_switch_info['dvs_name'])

    return task.info.result
