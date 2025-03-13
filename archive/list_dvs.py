

from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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



dvs_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                 [vim.DistributedVirtualSwitch],
                                                 True)

# delete all distributed virtual switches
for dvs in dvs_list.view:
    print(dvs.name)
dvs_list.Destroy()
