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


Usage: This is the list of student jump host VM names

'''

# Spine Leaf distributed Virtual Switch data base (Python dictionary)

dvs_info = [{"vnic": "vmnic7","dv_port_name":"LG01-DP-01","vlan_number": 10,"cluster_id":"LG01","dvs_name":"LG01-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG01-DP-02","vlan_number": 20,"cluster_id":"LG01","dvs_name":"LG01-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG02-DP-01","vlan_number": 10,"cluster_id":"LG02","dvs_name":"LG02-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG02-DP-02","vlan_number": 20,"cluster_id":"LG02","dvs_name":"LG02-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG03-DP-01","vlan_number": 10,"cluster_id":"LG03","dvs_name":"LG03-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG03-DP-02","vlan_number": 20,"cluster_id":"LG03","dvs_name":"LG03-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG04-DP-01","vlan_number": 10,"cluster_id":"LG04","dvs_name":"LG04-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG04-DP-02","vlan_number": 20,"cluster_id":"LG04","dvs_name":"LG04-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG05-DP-01","vlan_number": 10,"cluster_id":"LG05","dvs_name":"LG05-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG05-DP-02","vlan_number": 20,"cluster_id":"LG05","dvs_name":"LG05-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG06-DP-01","vlan_number": 10,"cluster_id":"LG06","dvs_name":"LG06-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG06-DP-02","vlan_number": 20,"cluster_id":"LG06","dvs_name":"LG06-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG07-DP-01","vlan_number": 10,"cluster_id":"LG07","dvs_name":"LG07-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG07-DP-02","vlan_number": 20,"cluster_id":"LG07","dvs_name":"LG07-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG08-DP-01","vlan_number": 10,"cluster_id":"LG08","dvs_name":"LG08-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG08-DP-02","vlan_number": 20,"cluster_id":"LG08","dvs_name":"LG08-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG09-DP-01","vlan_number": 10,"cluster_id":"LG09","dvs_name":"LG09-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG09-DP-02","vlan_number": 20,"cluster_id":"LG09","dvs_name":"LG09-dvs-2"},
            {"vnic": "vmnic7","dv_port_name":"LG10-DP-01","vlan_number": 10,"cluster_id":"LG10","dvs_name":"LG10-dvs-1"},
            {"vnic": "vmnic6","dv_port_name":"LG10-DP-02","vlan_number": 20,"cluster_id":"LG10","dvs_name":"LG10-dvs-2"}
]
