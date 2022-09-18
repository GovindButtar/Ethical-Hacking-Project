#!/bin/python
import nmap
import socket
import sys
if(len(sys.argv) == 4):
	target = socket.gethostbyname(sys.argv[1])
	min = str(sys.argv[2])
	max = str(sys.argv[3])
	portRange = min + "-" + max 
else:
	print("Invalid arguments")
nma = nmap.PortScannerAsync()
open_ports = {}
def callback_s(host, result):
	print(host, result)
	open_ports = result
print("Scanning " + target)
nma.scan(target, portRange, callback = callback_s)
while nma.still_scanning():
	nma.wait(0)
print("Scan done")
for host in open_ports['scan']:
            host_dict = open_ports['scan'][host]
            for port in filter(lambda x: host_dict['tcp'][x]['state'] == 'open',host_dict['tcp']):
                print(f"{port}: {host_dict['tcp'][port]['product']}")
