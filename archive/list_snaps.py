

from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

port="443"

sslContext = ssl._create_unverified_context()

si = SmartConnect(
    host='10.251.1.25',
    user='arubatm@vsphere.local',
    pwd='Aruba123!@#',
    port=port,
    sslContext=sslContext
)

content = si.RetrieveContent()

vm_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                 [vim.VirtualMachine],
                                                 True)
vm_data = vm_list.view

# These are the default snapshot names
afc_default_snapshot = "INITIAL"
psm_default_snapshot = "INITIAL"
workload_1_snapshot = "INITIAL"
workload_2_snapshot = "INITIAL"
workload_3_snapshot = "INITIAL"
workload_4_snapshot = "INITIAL"

# Look at list of all vm's and search their snapshosts for the ones we want.
for vm in vm_data:
    print(vm.name)
    print('=====================================================================')
