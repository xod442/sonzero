
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

'''
from flask import Flask, request, render_template, abort, redirect, url_for
import pymongo
import os
from jinja2 import Environment, FileSystemLoader
from bson.json_util import dumps
from bson.json_util import loads
from utility.switch_list import switch_list
from utility.get_logs2 import get_logs2
from utility.write_log import write_log
from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
from pyaoscx.session import Session
from pyaoscx.configuration import Configuration
from pyaoscx.device import Device
from pyaoscx.pyaoscx_factory import PyaoscxFactory
import urllib3
import datetime
from utility.cx_zero import cx_zero
from utility.vm_zero import vm_zero
from utility.cx_zero_group import cx_zero_group
from utility.vm_zero_group import vm_zero_group
# from utility.vm_jump_reset import vm_jump
from utility.cx_level201 import cx_level201
from utility.cx_level201_group import cx_level201_group
from utility.dvsx import makedvs
from utility.dvs_info import dvs_info
from utility.portgroup import makepgrp
from utility.deletedvs import deletedvs
import time
import subprocess
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#
app = Flask(__name__)

logging.basicConfig(filename="zero.log",
					format='%(asctime)s %(message)s',
					filemode='a')

db = {"switch_user": 'admin', 
       'switch_password' : 'admin',
       'vsphere_user': 'administrator@vsphere.local',
       'vsphere_pass' : 'Aruba123!@#',
       'vsphere_ip': '10.250.0.50'
       }


'''
#-------------------------------------------------------------------------------
Delete DVS
#-------------------------------------------------------------------------------
'''
@app.route("/dvsdelete", methods=('GET', 'POST'))
def dvsdelete(db):


    logging.basicConfig(filename="zero.log",
    					format='%(asctime)s %(message)s',
    					filemode='a')

    sslContext = ssl._create_unverified_context()

    port="443"

    # Create a connector to vsphere
    si = SmartConnect(
        host=db['vsphere_ip'],
        user=db['vsphere_user'],
        pwd=db['vsphere_pass'],
        port=port,
        sslContext=sslContext
    )

    content = si.RetrieveContent()
    dvs_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.DistributedVirtualSwitch],
                                                     True)

    for dvs in dvs_list.view:
        # rick.append('fail')

        # check, junk = dvs.name.split("-")
        message = 'Deleting distributed virtual switch %s' % (dvs.name)
        logging.warning(message)
        # if check == "dsf":
        task = dvs.Destroy_Task()
        response = WaitForTask(task)

    dvs_list.Destroy()


    when = str(datetime.datetime.now())
    message = "%s ==> All distributed virtual switches have been removed\n" % (when)
    logging.warning(message)
    response = write_log(db,message)

    Disconnect(si)

    message = "DVS have been deleted."
    return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
Test Route
#-------------------------------------------------------------------------------
'''

@app.route("/test", methods=('GET', 'POST'))
def test():
    return

'''
#-------------------------------------------------------------------------------
Main Page
#-------------------------------------------------------------------------------
'''

@app.route("/", methods=('GET', 'POST'))
def login():
    message = "Use reset menu top right to reset the lab"
    return render_template('home.html', message=message)

'''
#-------------------------------------------------------------------------------
Home
#-------------------------------------------------------------------------------
'''

@app.route("/home/<string:message>", methods=('GET', 'POST'))
def home(message):
    message = "User reset menu to Zero a lab group or a whole lab"
    return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
Reset Warning
#-------------------------------------------------------------------------------
'''

@app.route("/resetwarn>", methods=('GET', 'POST'))
def resetwarn():
    return render_template('resetwarn.html')


'''
#-------------------------------------------------------------------------------
Reset Lab
#-------------------------------------------------------------------------------
'''

@app.route("/zerolab>", methods=('GET', 'POST'))
def zerolab():

    # Start the lab resetting

    # Rollback CX switches
    response = cx_zero(db)

    #Reboot switches
    version='10.04'
    for switch in switch_list:
        subprocess.run(["python", "utility/boot_zero.py", switch, version, db['switch_user'], db['switch_password']])
        message = switch + ' was rebooted'
        logging.warning(message)
        response = write_log(db,message)

    # Reset VMware
    level = "INITIAL"
    response = vm_zero(db['vsphere_ip'], db['vsphere_user'], db['vsphere_pass'], level)

    # Delete any pre-existing DVS
    response = deletedvs(db)

    message = "The Lab has been completely reset"
    return render_template('home.html', message=message)

'''
#-------------------------------------------------------------------------------
Level up Lab
#-------------------------------------------------------------------------------
'''

@app.route("/leveluplab>", methods=('GET', 'POST'))
def leveluplab():

    # Start the lab resetting

    # Rollback CX switches
    response = cx_level201(db)

    #Reboot switches
    version='10.04'
    for switch in switch_list2:
        subprocess.run(["python", "utility/boot_zero.py", switch, version, db['switch_user'], db['switch_password']])
        message = switch + ' was rebooted'
        logging.warning(message)
        response = write_log(db,message)

    # Reset VMware
    level = "201LAB"
    response = vm_zero(db['vsphere_ip'], db['vsphere_user'], db['vsphere_pass'], level)

    # Build distributed virtual switches for spine leaf workshop.

    # Delete any pre-existing DVS
    response = deletedvs(db)

    sslContext = ssl._create_unverified_context()

    port="443"

    # Create a connector to vsphere
    si = SmartConnect(
        host=db['vsphere_ip'],
        user=db['vsphere_user'],
        pwd=db['vsphere_pass'],
        port=port,
        sslContext=sslContext
    )

    message="Starting to create distibuted virtual switches"
    logging.warning(message)

    for dvs in dvs_info:
        response = makedvs(si, dvs)
        time.sleep(3)

    message="Starting to port groups to distibuted virtual switches"
    logging.warning(message)

    #Build the port groups
    response = makepgrp(si)


    message = "The Lab is ready for the spine/leaf workshop"
    return render_template('home.html', message=message)
'''
#-------------------------------------------------------------------------------
Select Lab Group
#-------------------------------------------------------------------------------
'''

@app.route("/select_lab_group", methods=('GET', 'POST'))
def select_lab_group():

    message = "Select individual lab group to reset"
    return render_template('group_chooser.html', message=message)
'''
#-------------------------------------------------------------------------------
Select Lab Group to Level Up
#-------------------------------------------------------------------------------
'''

@app.route("/select_lab_level_group", methods=('GET', 'POST'))
def select_lab_level_group():

    message = "Select individual lab group TE4.202 Spine/Leaf"
    return render_template('group_level_chooser.html', message=message)

'''
#-------------------------------------------------------------------------------
Select Lab Group to boot switches
#-------------------------------------------------------------------------------
'''

@app.route("/boot_lab_group_switches", methods=('GET', 'POST'))
def boot_lab_group_switches():

    message = "Select individual lab group switches to reboot"
    return render_template('group_switch_boot.html', message=message)

'''
#-------------------------------------------------------------------------------
Reset Lab Group
#-------------------------------------------------------------------------------
'''


@app.route("/reset_lab_group", methods=('GET', 'POST'))
def reset_lab_group():

    group = request.form['group']

    if group == "LG01":
        lab_switch_list = ["10.250.201.101","10.250.201.102"]
        lab_vm_names = ["LG01-PSM","LG01-AFC","LG01-WL01-V10-101","LG01-WL02-V10-102"]
        dvs_name = 'dsf-leaf01'
        message = 'Lab Group 01 has been reset to vm_zero'

    if group == "LG02":
        lab_switch_list = ["10.250.202.101","10.250.202.102"]
        lab_vm_names = ["LG02-PSM","LG02-AFC","LG02-WL01-V10-101","LG02-WL02-V10-102"]
        dvs_name = 'dsf-leaf02'
        message = 'Lab Group 02 has been reset to vm_zero'

    if group == "LG03":
        lab_switch_list = ["10.250.203.101","10.250.203.102"]
        lab_vm_names = ["LG03-PSM","LG03-AFC","LG03-WL01-V10-101","LG03-WL02-V10-102"]
        dvs_name = 'dsf-leaf03'
        message = 'Lab Group 03 has been reset to vm_zero'

    if group == "LG04":
        lab_switch_list = ["10.250.204.101","10.250.204.102"]
        lab_vm_names = ["LG04-PSM","LG04-AFC","LG04-WL01-V10-101","LG04-WL02-V10-102"]
        dvs_name = 'dsf-leaf04'
        message = 'Lab Group 04 has been reset to vm_zero'

    if group == "LG05":
        lab_switch_list = ["10.250.205.101","10.250.205.102"]
        lab_vm_names = ["LG05-PSM","LG05-AFC","LG05-WL01-V10-101","LG05-WL02-V10-102"]
        dvs_name = 'dsf-leaf05'
        message = 'Lab Group 05 has been reset to vm_zero'

    if group == "LG06":
        lab_switch_list = ["10.250.206.101","10.250.206.102"]
        lab_vm_names = ["LG06-PSM","LG06-AFC","LG06-WL01-V10-101","LG06-WL02-V10-102"]
        dvs_name = 'dsf-leaf06'
        message = 'Lab Group 06 has been reset to vm_zero'

    if group == "LG07":
        lab_switch_list = ["10.250.207.101","10.250.207.102"]
        lab_vm_names = ["LG07-PSM","LG07-AFC","LG07-WL01-V10-101","LG07-WL02-V10-102"]
        dvs_name = 'dsf-leaf07'
        message = 'Lab Group 07 has been reset to vm_zero'

    if group == "LG08":
        lab_switch_list = ["10.250.208.101","10.250.208.102"]
        lab_vm_names = ["LG08-PSM","LG08-AFC","LG08-WL01-V10-101","LG08-WL02-V10-102"]
        dvs_name = 'dsf-leaf08'
        message = 'Lab Group 08 has been reset to vm_zero'

    if group == "LG09":
        lab_switch_list = ["10.250.209.101","10.250.209.102"]
        lab_vm_names = ["LG09-PSM","LG09-AFC","LG09-WL01-V10-101","LG09-WL02-V10-102"]
        dvs_name = 'dsf-leaf09'
        message = 'Lab Group 09 has been reset to vm_zero'

    if group == "LG10":
        lab_switch_list = ["10.250.210.101","10.250.210.102"]
        lab_vm_names = ["LG10-PSM","LG10-AFC","LG10-WL01-V10-101","LG10-WL02-V10-102"]
        dvs_name = 'dsf-leaf10'
        message = 'Lab Group 10 has been reset to vm_zero'


    # Get credentials

    vsphere_user = db['vsphere_user']
    vsphere_pass = db['vsphere_password']
    switch_user = db['switch_user']
    switch_password = db['switch_password']

    # Get IP vsphere
    vsphere_ip = db['vsphere_ip']

    # Start the lab resetting

    # Rollback CX switches
    response = cx_zero_group(switch_user, switch_password, lab_switch_list)

    #Reboot switches
    version='10.04'
    for switch in lab_switch_list:
        response = subprocess.run(["python", "utility/boot_zero.py", switch, version, switch_user, switch_password])
        message = switch + 'was rebooted'
        logging.warning(message)
        response = write_log(db,message)

    # Reset VMware
    level = "INITIAL"
    response = vm_zero_group(vsphere_ip, vsphere_user, vsphere_pass, lab_vm_names, dvs_name, level, db)

    message = "Individual Lab has been completely reset"
    return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
Boot lab group switches
#-------------------------------------------------------------------------------
'''


@app.route("/group_boot_switches", methods=('GET', 'POST'))
def group_boot_switches():

    group = request.form['group']

    switch_user = db['switch_user']
    switch_password = db['switch_password']


    if group == "LG01":
        lab_switch_list = ["10.250.201.101","10.250.201.102"]
        message = 'Lab Group 01 has been booted'

    if group == "LG02":
        lab_switch_list = ["10.250.202.101","10.250.202.102"]
        message = 'Lab Group 02 has been booted'

    if group == "LG03":
        lab_switch_list = ["10.250.203.101","10.250.203.102"]
        message = 'Lab Group 03 has been booted'

    if group == "LG04":
        lab_switch_list = ["10.250.204.101","10.250.204.102"]
        message = 'Lab Group 04 has been booted'

    if group == "LG05":
        lab_switch_list = ["10.250.205.101","10.250.205.102"]
        message = 'Lab Group 05 has been booted'

    if group == "LG06":
        lab_switch_list = ["10.250.206.101","10.250.206.102"]
        message = 'Lab Group 06 has been booted'

    if group == "LG07":
        lab_switch_list = ["10.250.207.101","10.250.207.102"]
        message = 'Lab Group 07 has been booted'

    if group == "LG08":
        lab_switch_list = ["10.250.208.101","10.250.208.102"]
        message = 'Lab Group 08 has been booted'

    if group == "LG09":
        lab_switch_list = ["10.250.209.101","10.250.209.102"]
        message = 'Lab Group 09 has been booted'

    if group == "LG10":
        lab_switch_list = ["10.250.210.101","10.250.210.102"]
        message = 'Lab Group 10 has been booted'

    # Start booting the switches

    #Reboot switches
    version='10.04'
    for switch in lab_switch_list:
        response = subprocess.run(["python", "utility/boot_zero.py", switch, version, switch_user, switch_password])
        message = switch + 'was rebooted'
        logging.warning(message)
        response = write_log(db,message)

    message = "Individual Lab switches have been booted"
    return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
201LAB Lab Group
#-------------------------------------------------------------------------------
'''


@app.route("/lab201_lab_group", methods=('GET', 'POST'))
def lab201_lab_group():

    group = request.form['group']

    vsphere_user = db['vsphere_user']
    vsphere_pass = db['vsphere_password']
    switch_user = db['switch_user']
    switch_password = db['switch_password']

    # Get IP vsphere
    vsphere_ip = db['vsphere_ip']

    if group == "LG01":
        lab_switch_list = ["10.250.201.101","10.250.201.102"]
        lab_vm_names = ["LG01-PSM","LG01-AFC","LG01-WL01-V10-101","LG01-WL02-V10-102"]
        dvs_name = 'dsf-leaf01'
        message = 'Lab Group 01 has been reset to vm_zero'

    if group == "LG02":
        lab_switch_list = ["10.250.202.101","10.250.202.102"]
        lab_vm_names = ["LG02-PSM","LG02-AFC","LG02-WL01-V10-101","LG02-WL02-V10-102"]
        dvs_name = 'dsf-leaf02'
        message = 'Lab Group 02 has been reset to vm_zero'

    if group == "LG03":
        lab_switch_list = ["10.250.203.101","10.250.203.102"]
        lab_vm_names = ["LG03-PSM","LG03-AFC","LG03-WL01-V10-101","LG03-WL02-V10-102"]
        dvs_name = 'dsf-leaf03'
        message = 'Lab Group 03 has been reset to vm_zero'

    if group == "LG04":
        lab_switch_list = ["10.250.204.101","10.250.204.102"]
        lab_vm_names = ["LG04-PSM","LG04-AFC","LG04-WL01-V10-101","LG04-WL02-V10-102"]
        dvs_name = 'dsf-leaf04'
        message = 'Lab Group 04 has been reset to vm_zero'

    if group == "LG05":
        lab_switch_list = ["10.250.205.101","10.250.205.102"]
        lab_vm_names = ["LG05-PSM","LG05-AFC","LG05-WL01-V10-101","LG05-WL02-V10-102"]
        dvs_name = 'dsf-leaf05'
        message = 'Lab Group 05 has been reset to vm_zero'

    if group == "LG06":
        lab_switch_list = ["10.250.206.101","10.250.206.102"]
        lab_vm_names = ["LG06-PSM","LG06-AFC","LG06-WL01-V10-101","LG06-WL02-V10-102"]
        dvs_name = 'dsf-leaf06'
        message = 'Lab Group 06 has been reset to vm_zero'

    if group == "LG07":
        lab_switch_list = ["10.250.207.101","10.250.207.102"]
        lab_vm_names = ["LG07-PSM","LG07-AFC","LG07-WL01-V10-101","LG07-WL02-V10-102"]
        dvs_name = 'dsf-leaf07'
        message = 'Lab Group 07 has been reset to vm_zero'

    if group == "LG08":
        lab_switch_list = ["10.250.208.101","10.250.208.102"]
        lab_vm_names = ["LG08-PSM","LG08-AFC","LG08-WL01-V10-101","LG08-WL02-V10-102"]
        dvs_name = 'dsf-leaf08'
        message = 'Lab Group 08 has been reset to vm_zero'

    if group == "LG09":
        lab_switch_list = ["10.250.209.101","10.250.209.102"]
        lab_vm_names = ["LG09-PSM","LG09-AFC","LG09-WL01-V10-101","LG09-WL02-V10-102"]
        dvs_name = 'dsf-leaf09'
        message = 'Lab Group 09 has been reset to vm_zero'

    if group == "LG10":
        lab_switch_list = ["10.250.210.101","10.250.210.102"]
        lab_vm_names = ["LG10-PSM","LG10-AFC","LG10-WL01-V10-101","LG10-WL02-V10-102"]
        dvs_name = 'dsf-leaf10'
        message = 'Lab Group 10 has been reset to vm_zero'


    # Start the lab resetting

    # Rollback CX switches
    response = cx_level201_group(switch_user, switch_password, lab_switch_list)

    #Reboot switches
    version='10.04'
    for switch in lab_switch_list:
        response = subprocess.run(["python", "utility/boot_zero.py", switch, version, switch_user, switch_password])
        message = switch + 'was rebooted'
        logging.warning(message)
        response = write_log(db,message)

    # Reset VMware
    level = "201LAB"
    response = vm_zero_group(vsphere_ip, vsphere_user, vsphere_pass, lab_vm_names, dvs_name, level)

    message = "Individual Lab has been completely reset"
    return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
Labs
#-------------------------------------------------------------------------------
'''




@app.route("/select_level", methods=('GET', 'POST'))
def select_level():

    level = request.form['level']
    if level == "1":
        message = 'Lab 1 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "2":
        message = 'Lab 2 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "3":
        message = 'Lab 3 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "4":
        message = 'Lab 4 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "5":
        message = 'Lab 5 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "6":
        message = 'Lab 6 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "7":
        message = 'Lab 7 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "8":
        message = 'Lab 8 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
    if level == "9":
        message = 'Lab 9 complete. Proceed with Workshop'
        return render_template('return.html', message=message)
