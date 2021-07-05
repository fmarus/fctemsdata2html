# fctemsdata2html
ctemsepdata2html.py - FortiClient EMS tool to import Endpoint Data and extract it into HTML format.
Usage: fctemsepdata2html.py <hostname> <username> <password> <file_output> <offset> <count>[<port>]
<hostname>: FortiClient EMS server FQDN/IP Address 
<username>: FortiClient EMS Administrator Username
<password>: Administrator password
<file_output>: Output file name
<offset>: Start index of FortiClient EMS Endpoint Data array
<count>: Number of Endpoint Data to be collected
Optional:
<port>: Custom FortiClient EMS HTTP Port (default=443)
  #Installation
  pip3 install -r requirements.txt
