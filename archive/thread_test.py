#!/usr/bin/env python3

# Released under MIT License

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

Note: A test script to boot a list of switches

'''
from utility.boot_switch import boot_switch
import concurrent.futures

version = "10.04"
switch_user = "admin"
switch_password = "admin"

# Create a list of switch information
switch_info=[
        ["10.251.1.12", version, switch_user, switch_password],
        ["10.251.1.11", version, switch_user, switch_password],
        ["10.251.1.13", version, switch_user, switch_password]
    ]


# Retrieve a single page and report the URL and contents
def booter(self, switch):
    ip, version, switch_user, switch_password = switch
    bootx = boot_switch(self, ip, version, switch_user, switch_password)
    print(bootx)
    return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(booter, switch, 60): switch for switch in switch_info}
    for future in concurrent.futures.as_completed(future_to_url):
        response = future_to_url[future]
        #print(response)
        '''
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (response, exc))
        else:
            print(response)
        '''
