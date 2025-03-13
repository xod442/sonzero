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


Usage: This python file is several lists of outlet information for the PDU's in the vlab

'''
# edit this list of PDU Ip addresses
pdu_list = ['https://10.202.63.10','https://10.202.63.12']

# These are the outlets on the PDU that will be turned ON & OFF!
port_list = [7,9,10,11,12,13,14,15,16,18,19,20,21,22,23]

# A list of OUTLET by name
outlet_list = ["OUTLET7",
               "OUTLET9",
               "OUTLET10",
               "OUTLET11",
               "OUTLET12",
               "OUTLET13",
               "OUTLET14",
               "OUTLET15",
               "OUTLET16",
               "OUTLET18",
               "OUTLET19",
               "OUTLET20",
               "OUTLET21",
               "OUTLET22",
               "OUTLET23"
]
outlet_name_list = ["OUTLETSeven",
                    "OUTLETNine",
                    "OUTLETTen",
                    "OUTLETEleven",
                    "OUTLETTwelve",
                    "OUTLETThirteen",
                    "OUTLETFourteen",
                    "OUTLETFifteen",
                    "OUTLETSixteen",
                    "OUTLETEighteen",
                    "OUTLETNineteen",
                    "OUTLETTwenty",
                    "OUTLETTwentyOne",
                    "OUTLETTwentyTwo",
                    "OUTLETTwentyThree"                    
]
