'''
888888888888                                      88              88
         ,88                                      88              88
       ,88"                                       88              88
     ,88"     ,adPPYba,  8b,dPPYba,   ,adPPYba,   88  ,adPPYYba,  88,dPPYba,
   ,88"      a8P_____88  88P'   "Y8  a8"     "8a  88  ""     `Y8  88P'    "8a
 ,88"        8PP"""""""  88          8b       d8  88  ,adPPPPP88  88       d8
88"          "8b,   ,aa  88          "8a,   ,a8"  88  88,    ,88  88b,   ,a8"
888888888888  `"Ybbd8"'  88           `"YbbdP"'   88  `"8bbdP"Y8  8Y"Ybbd8"'

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to
do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Written by Rick Kauffman
Github: https://github.com/xod442/zero.git

Note: A script to fetch logs from the mongoDB

'''
from pyVmomi import vim
from pyVim.task import WaitForTask
from pyVim.connect import SmartConnect, Disconnect
import ssl
import time
import logging
from bson.json_util import dumps
from bson.json_util import loads
import datetime
from utility.write_log import write_log
#Script to get all logs from database
def deletedvs(db):

    # Get credentials
    get_creds = db.creds.find({})
    json_creds = loads(dumps(get_creds))
    vsphere_user = json_creds[0]['vuser']
    vsphere_pass = json_creds[0]['vsphere_password']

    # Get IP vsphere
    get_ips = db.address.find({})
    json_ips = loads(dumps(get_ips))
    vsphere_ip = json_ips[0]['vip']

    logging.basicConfig(filename="zero.log",
    					format='%(asctime)s %(message)s',
    					filemode='a')

    sslContext = ssl._create_unverified_context()

    port="443"

    # Create a connector to vsphere
    si = SmartConnect(
        host=vsphere_ip,
        user=vsphere_user,
        pwd=vsphere_pass,
        port=port,
        sslContext=sslContext
    )

    content = si.RetrieveContent()
    dvs_list = content.viewManager.CreateContainerView(content.rootFolder,
                                                     [vim.DistributedVirtualSwitch],
                                                     True)

    for dvs in dvs_list.view:

        message = 'Deleting distributed virtual switch %s' % (dvs.name)
        logging.warning(message)
        task = dvs.Destroy_Task()
        response = WaitForTask(task)

    dvs_list.Destroy()


    when = str(datetime.datetime.now())
    message = "%s ==> All distributed virtual switches have been removed\n" % (when)
    logging.warning(message)
    response = write_log(db,message)

    Disconnect(si)

    message = "DVS have been deleted."
    return message
