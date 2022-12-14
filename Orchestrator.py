#!/bin/python3
import nmap
import socket
import sys
import asyncio
import subprocess
import urllib.parse
import pandas as pd
async def main():
    print(sys.argv[1])
    if(len(sys.argv) == 4): #4
        hostname = urllib.parse.urlparse(sys.argv[1])
        print("hostname: " + str(hostname))
        target = socket.gethostbyname(hostname.netloc)
        print("target: " + str(target))
        min = str(sys.argv[2])
        max = str(sys.argv[3])
        portRange = min + "-" + max 
    else:
        print("Invalid arguments")
    nma = nmap.PortScanner() 
    open_ports = []
    nma.scan(target, portRange)
    for host in nma.all_hosts():
        host_dict = nma[host]
        for port in filter(lambda x: host_dict['tcp'][x]['state'] == "open", host_dict['tcp']):
            open_ports.append(port)
            print(open_ports)
            print("starting Nikto")
            NiktoOutput = await asyncio.create_subprocess_shell("nikto" + " -h "+ str(socket.gethostbyname(urllib.parse.urlparse(sys.argv[1]).netloc)) + " -p " + str(port) + " -C all -o " + "NiktoOutput.csv")
    print("starting Ferox")
    FeroxOutput = await asyncio.create_subprocess_shell("feroxbuster " + " -u " + str(sys.argv[1]) + " --extract-links --silent -s 200 301 302 -x pdf -x js html -x php txt json docx fff -s 200 --filter-regex '=>' -o FeroxFile.csv | python3 sqlmap.py")
    await NiktoOutput.wait()
    await FeroxOutput.wait()
    print(NiktoOutput)
    print(FeroxOutput)
    FeroxFile = pd.read_csv("FeroxFile.csv")
    blacklist = ["MSG", "=>"]
    FeroxFile = FeroxFile[FeroxFile.apply(lambda col: col.isin(blacklist) == False)]
    textFile = open("SQLMapSetup.txt", 'a')
    textFile.write(FeroxFile.to_string())
    print("Pandas FeroxFile")
    print(FeroxFile)
    print("SQL setup")
    print(textFile)
    textFile.close()
asyncio.run(main())
