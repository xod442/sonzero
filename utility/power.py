

from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
import urllib3
import logging


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(filename="zero.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

port="443"

sslContext = ssl._create_unverified_context()

si = SmartConnect(
    host='10.250.0.50',
    user='administrator@vsphere.local',
    pwd='Aruba123!@#',
    port=port,
    sslContext=sslContext
)

content = si.RetrieveContent()

vm_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                 [vim.VirtualMachine],
                                                 True)
vm_data = vm_list.view

for vm in vm_data:
    if vm:
        # Get the current power state of the virtual machine
        power_state = vm.runtime.powerState
        if power_state != vim.VirtualMachinePowerState.poweredOn:
            message = "VM Name is %s => is NOT powered on!......." % (vm.name)
            logging.warning(message)
