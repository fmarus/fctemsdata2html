#!/usr/bin/env python3
# fctemsepdata2html.py
# by fmarus (github.com/fmarus) and TAS (github.com/jajalcoding)
# version 0.1
# tested on python3.9 and FortiClient EMS 7.0
# To-do List:
# - cmd line argv enhancement
# - password handling
# - response code/error handling (200/40x/500)

import requests
import json
import sys
import html
import datetime
from json2html import *
#import pdb

requests.urllib3.disable_warnings()

try:
    host=sys.argv[1]
    username=sys.argv[2]
    password=sys.argv[3]
    file_output=sys.argv[4]
    offset=sys.argv[5]
    count=sys.argv[6]
except:
    print("fctemsepdata2html.py - FortiClient EMS tool to import Endpoint Data and extract it into HTML format.")
    print("Usage: fctemsepdata2html.py <hostname> <username> <password> <file_output> <offset> <count>[<port>]")
    print("<hostname>: FortiClient EMS server FQDN/IP Address ")
    print("<username>: FortiClient EMS Administrator Username")
    print("<password>: Administrator password")   
    print("<file_output>: Output file name")
    print("<offset>: Start index of FortiClient EMS Endpoint Data array")
    print("<count>: Number of Endpoint Data to be collected")
    print("Optional:")
    print("<port>: Custom FortiClient EMS HTTP Port (default=443)")
    print("Example: python3 fctemsepdata2html.py ems.ftnt.local admin password epdata.html 0 30 ")
    print("")
    exit()

base_port="443"
base_url="https://"+host+':'+base_port
path_login="/api/v1/auth/signin"
path_logout="/api/v1/auth/signout"
path_endpoint="/api/v1/endpoints/index?offset="+offset+"&count="+count
ems_site="Default"

## LOGIN
url = base_url+path_login
payload='name='+username+'&password='+password+'&site='+ems_site
headers = {
  'Ems-Call-Type': '2',
  'Content-Type': 'application/x-www-form-urlencoded'
}
print("Logging in...")
try:
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
except:
    print("FAILED: Server not found")
    exit()

cookie = response.cookies.get_dict()
print("...done")
## GET EP Entry
print("Getting Endpoint Data...")
url = base_url+path_endpoint

payload={}
headers = {
  'Ems-Call-Type': '2'
}
response = requests.request("GET", url, headers=headers, data=payload, verify=False, cookies=cookie)
print("...done")
print("Converting to HTML...")

infoFromJson = json.loads(response.text)

filtered = infoFromJson['data']['endpoints']
filtered2=[]
for i in filtered:
    i['last_seen'] = datetime.datetime.fromtimestamp(i['last_seen']).strftime('%A, %d %B %Y %H:%M:%S')
    if not i['avatar']==None:
        i['avatar']='<img src="'+i['avatar']+'"></img>'
    
    filtered2.append( {'Name': i['name'], 'Username': i['username'], 'Avatar': i['avatar'], 'IP Address': i['ip_addr'], 'Group Path': i['group_path'], 'FortiClient Version': i['fct_version'], 'OS Version': i['os_version'], 'Last Seen': i['last_seen']}  )

formatted = json2html.convert(json = filtered2, table_attributes="class=\"table table-bordered table-hover\"")
# pdb.set_trace()
# replace named and numeric character references to proper Unicode characters
# opt 1 using formatted.replace
# formatted = formatted.replace('&quot;', '"')
# formatted = formatted.replace('&gt;', '>')
# formatted = formatted.replace('&lt;', '<')
# opt 2 using html.unescape()
formatted = html.unescape(formatted)

your_file = open(file_output,"w")
your_file.write("""<!doctype html>
<html>
<head>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
 
<!-- Optional theme -->
<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css">
 
</head><body>
<!-- Latest compiled and minified JavaScript -->
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
""")
your_file.write(formatted)
your_file.write('</body></html>')
your_file.close()
print("...done")

## LOGOUT
url = base_url+path_logout
response = requests.request("GET", url, headers=headers, data=payload, verify=False, cookies=cookie)
#print(response.text)
print("Logged out")