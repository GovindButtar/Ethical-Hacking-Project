#!/bin/python
import nmap
import socket
import sys
import asyncio
import subprocess
if(len(sys.argv) == 4):
	target = socket.gethostbyname(sys.argv[1])
	min = str(sys.argv[2])
	max = str(sys.argv[3])
	portRange = min + "-" + max 
else:
	print("Invalid arguments")
nma = nmap.PortScannerAsync() 
open_ports = []
def callback_s(host, result):
	print(host, result)
	for host in result['scan']:
            host_dict = result['scan'][host]
            for port in filter(lambda x: host_dict['tcp'][x]['state'] == 'open',host_dict['tcp']):
            	open_ports.append(port)
            	print(open_ports)
            	print("Running FeroxBuster")
            	for i in open_ports:
            		runFeroxBuster(sys.argv[1], i)
print("Scanning " + target)
nma.scan(target, portRange, callback=callback_s)
while nma.still_scanning():
	nma.wait(0)
print("Scan done")

async def runFeroxBuster(hostname, port):
	subprocess.run("./feroxbuster -u "+ hostname + ":" + port + " -x pdf -x js,html -x php txt json,docx")
