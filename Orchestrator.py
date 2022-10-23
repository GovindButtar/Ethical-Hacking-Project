#!/bin/python3
import nmap
import socket
import sys
import asyncio
import subprocess
import urllib.parse
async def main():
    if(len(sys.argv) == 4):
        hostname = urllib.parse.urlparse(sys.argv[1])
        target = socket.gethostbyname(hostname.netloc)
        min = str(sys.argv[2])
        max = str(sys.argv[3])
        portRange = min + "-" + max 
    else:
        print("Invalid arguments")
    nma = nmap.PortScanner() 
    open_ports = []
    print("Scanning " + target)
    nma.scan(target, portRange)
    for host in nma.all_hosts():
        host_dict = nma[host]
        for port in filter(lambda x: host_dict['tcp'][x]['state'] == "open", host_dict['tcp']):
            open_ports.append(port)
            print(open_ports)
            NiktoOutput = asyncio.create_task(runNiktoScan(port))
    FeroxOutput = asyncio.create_task(runFeroxBuster())
    await NiktoOutput
    await FeroxOutput

    print("Scan done")
async def runNiktoScan(port):
    print("nikto")
    output = subprocess.run(["nikto", "-h", str(target), "-p", str(port), "-o", "NiktoOutput.txt"])
    return output
async def runFeroxBuster():
    print("ferox")
    output = subprocess.run(["feroxbuster", "-u", str(sys.argv[1]), "-x", "pdf", "-x", "js",",html","-x","php","txt","json",",docx", "-o", "FeroxFile.txt"]) #return await
    return output

asyncio.run(main())
# OpenSSH: 22
# Apache httpd: 80
