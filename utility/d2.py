from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import ssl

def add_distributed_virtual_switch(
        host, username, password, datacenter_name, dvs_name, dvs_version):
    try:
        # Disable SSL certificate verification (not recommended for production)
        context = ssl._create_unverified_context()
        context.verify_mode = ssl.CERT_NONE

        # Connect to vCenter Server
        service_instance = SmartConnect(
            host=host, user=username, pwd=password, sslContext=context)

        if not service_instance:
            raise Exception("Failed to connect to vCenter Server")

        # atexit.register(Disconnect, service_instance)

        # Get the datacenter object
        datacenter = service_instance.content.rootFolder.childEntity[0]
        for dc in datacenter.vmFolder.childEntity:
            if dc.name == datacenter_name:
                datacenter = dc
                break

        # Create a DVS config spec
        dvs_spec = vim.DistributedVirtualSwitch.ConfigSpec()
        dvs_spec.name = dvs_name
        dvs_spec.configVersion = dvs_version

        # Create the DVS
        dvs = datacenter.networkFolder.CreateDVS_Task(spec=dvs_spec)

        print(f"Distributed Virtual Switch '{dvs_name}' created successfully.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # VMware vCenter Server information
    vcenter_host = "10.250.0.50"
    vcenter_user = "administrator@vsphere.local"
    vcenter_password = "Aruba123!@#"

    # Datacenter where you want to create the DVS
    datacenter_name = "DCN-ILT-VLAB"

    # DVS settings
    dvs_name = "YourDVSName"
    dvs_version = "7.0.0"

    add_distributed_virtual_switch(
        vcenter_host, vcenter_user, vcenter_password, datacenter_name, dvs_name, dvs_version)
