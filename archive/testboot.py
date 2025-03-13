
from utility.switch_list import switch_list
from time import sleep
import subprocess

switch_user='admin'
switch_password = 'admin'
# switch_list=["10.250.210.101","10.250.210.102"]
version='10.09'

db ='me'
for switch in switch_list:
    myList = [switch,version,switch_user,switch_password,db]
    subprocess.run(["python", "utility/boot_zero.py", switch, version, switch_user, switch_password, db])
