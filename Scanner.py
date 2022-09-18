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
def callback_s(host, result):
	print(host, result)
print("Scanning " + target)
nma.scan(target, portRange, callback = callback_s)
while nma.still_scanning():
	nma.wait(0)
print("Scan done")