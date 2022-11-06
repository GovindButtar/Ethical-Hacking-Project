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
            print("starting Nikto")
            NiktoOutput = await asyncio.create_subprocess_shell("nikto" + " -h "+ str(socket.gethostbyname(urllib.parse.urlparse(sys.argv[1]).netloc)) + " -p " + str(port) + " -o " + "NiktoOutput.txt")
    print("starting Ferox")
    FeroxOutput = await asyncio.create_subprocess_shell("feroxbuster " + " -u " + str(sys.argv[1]) + " -x pdf -x js html -x php txt json docx fff -s 200 -o FeroxFile.txt")
    await NiktoOutput.wait()
    await FeroxOutput.wait()
    print(FeroxOutput)
    print("Scan done")
asyncio.run(main())
