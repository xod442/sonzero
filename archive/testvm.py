from utility.vm_zero import vm_zero

vsphere_user='administrator@vsphere.local'
vsphere_password = 'Aruba123!@#'
vsphere_ip = '10.250.0.50'

db ='me'

response = vm_zero(vsphere_ip, vsphere_user, vsphere_password, db)

print(response)
