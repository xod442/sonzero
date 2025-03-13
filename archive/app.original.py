
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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#
app = Flask(__name__)

# A dictionary of the mongo database credentials
config = {
    "username": "admin",
    "password": "siesta3",
    "server": "mongo",
}

# Setup database connetor
connector = "mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])
client = pymongo.MongoClient(connector)

#set mongo database
db = client["zero"]

'''
#-------------------------------------------------------------------------------
Main Page
#-------------------------------------------------------------------------------
'''

@app.route("/", methods=('GET', 'POST'))
def login():
    if db.creds.count_documents({}) > 0:
        message = "Select the AFC lab level"
        return render_template('home.html', message=message)
    else:
        return render_template('creds.html')

'''
#-------------------------------------------------------------------------------
Home
#-------------------------------------------------------------------------------
'''

@app.route("/home/<string:message>", methods=('GET', 'POST'))
def home(message):


    message = "Select the AFC lab level"
    return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
Creds
#-------------------------------------------------------------------------------
'''

@app.route("/add_creds", methods=('GET', 'POST'))
def add_creds():
    db.creds.drop()

    entry = {
        "vuser": request.form['vuser'].replace("'", ""),
        "vsphere_password": request.form['vsphere_password'].replace("'", ""),
        "switch_user": request.form['switch_user'].replace("'", ""),
        "switch_password": request.form['switch_password'].replace("'", ""),
    }
    res = db.creds.insert_one(entry)

    message = "Credentials have been saved in the database"
    return render_template('address.html', message=message)

@app.route("/reset_creds", methods=('GET', 'POST'))
def reset_creds():
    return render_template('creds_reset.html')

@app.route("/reset_creds_only", methods=('GET', 'POST'))
def creds_reset_only():
    db.creds.drop()

    entry = {
        "vuser": request.form['vuser'].replace("'", ""),
        "vsphere_password": request.form['vsphere_password'].replace("'", ""),
        "switch_user": request.form['switch_user'].replace("'", ""),
        "switch_password": request.form['switch_password'].replace("'", ""),
    }
    res = db.creds.insert_one(entry)

    message = "Credentials have been saved in the database"
    return render_template('home.html', message=message)

'''
#-------------------------------------------------------------------------------
IP Addresses
#-------------------------------------------------------------------------------
'''

@app.route("/add_address", methods=('GET', 'POST'))
def add_address():
    db.address.drop()

    entry = {
        "vip": request.form['vip'].replace("'", "")
    }
    res = db.address.insert_one(entry)

    message = "IP addresses have been saved in the database"
    return render_template('home.html', message=message)

@app.route("/address_reset", methods=('GET', 'POST'))
def address_reset():
    message = "Enter the IP address information for the vSphere console"
    return render_template('address.html', message=message)

'''
#-------------------------------------------------------------------------------
Logs
#-------------------------------------------------------------------------------
'''

@app.route("/get_logs", methods=('GET', 'POST'))
def get_logs():
    logs = get_logs2(db)
    return render_template('list_logs.html', logs=logs)

@app.route("/delete_logs", methods=('GET', 'POST'))
def delete_logs():
    db.log.drop()
    message = "Logs database has been deleted"
    return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
Reset Lab
#-------------------------------------------------------------------------------
'''

@app.route("/zerolab>", methods=('GET', 'POST'))
def zerolab():
    db.log.drop()

    # Get credentials
    get_creds = db.creds.find({})
    json_creds = loads(dumps(get_creds))
    vsphere_user = json_creds[0]['vuser']
    vsphere_pass = json_creds[0]['vsphere_password']
    switch_user = json_creds[0]['switch_user']
    switch_password = json_creds[0]['switch_password']

    # Get IP vsphere
    get_ips = db.address.find({})
    json_ips = loads(dumps(get_ips))
    vsphere_ip = json_ips[0]['vip']

    port="443"
    version = '10.04'

    # Set process Level
    level = 'INITIAL'

    sslContext = ssl._create_unverified_context()

    # Create a connector to vsphere
    si = SmartConnect(
        host=vsphere_ip,
        user=vsphere_user,
        pwd=vsphere_pass,
        port=port,
        sslContext=sslContext
    )



    #---------------------------------------------------------------------------
    #
    #   Step 1: Revert and Reset Virtual Machines
    #   TODO: Make module and pass it si, level, and db vars
    #---------------------------------------------------------------------------

    content = si.RetrieveContent()

    vm_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.VirtualMachine],
                                                     True)
    vm_data = vm_list.view


    # revert all vms to snapshot named INITIAL and reboot or reset vm.
    for vm in vm_data:
        if vm.snapshot:
            snapshot_list = vm.snapshot.rootSnapshotList
            if snapshot_list:
                for snapshot in snapshot_list:
                    if snapshot.name == level:
                        response = revert_vm(snapshot.snapshot)
                        # reboot vm
                        try:
                            vm.RebootGuest()
                        except:
                            # forceably shutoff/on
                            # need to do if vmware guestadditions isn't running
                            vm.ResetVM_Task()
                        # Compose log information
                        when = str(datetime.datetime.now())
                        message = "%s ==> vm: %s has been reverted and rebooted\n" % (when,vm)
                        response = write_log(db,message)
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
        task = dvs.Destroy_Task()
        response = WaitForTask(task)
    dvs_list.Destroy()

    si.Disconnect()

    when = str(datetime.datetime.now())
    message = "%s ==> All distributed virtual switches have been removed\n" % (when)
    response = write_log(db,message)

    # from the utility/switch_list.py get a list of switches to rollback to zero
    #---------------------------------------------------------------------------
    #
    #   Step 3: Rollback and Reset switches
    #
    #---------------------------------------------------------------------------

    for switch in switch_list:
        s = Session(ip, version)
        s.open(switch_user, switch_password)
        config_obj = Configuration(s)
        reponse = config_obj.create_checkpoint('ZERO', 'startup-config')
        s.close()

        when = str(datetime.datetime.now())
        message = "%s ==> All All switches have been checkpointe\n" % (when)
        response = write_log(db,message)

    #---------------------------------------------------------------------------
    #
    #   Step 4: Turn ports on PDU on and off to force boot switches
    #
    #---------------------------------------------------------------------------

    # TODO ADD code


    message = "The lab has been completely reset"
    return render_template('home.html', message=message)




'''
#-------------------------------------------------------------------------------
Levels
#-------------------------------------------------------------------------------
'''



@app.route("/select_level", methods=('GET', 'POST'))
def select_level():
    level = request.form['level']
    if level == "1":
        message = 'Level 1 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "2":
        message = 'Level 2 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "3":
        message = 'Level 3 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "4":
        message = 'Level 4 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "5":
        message = 'Level 5 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "6":
        message = 'Level 6 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "7":
        message = 'Level 7 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "8":
        message = 'Level 8 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
    if level == "9":
        message = 'Level 9 complete. Go to https://10.251.1.25'
        return render_template('return.html', message=message)
