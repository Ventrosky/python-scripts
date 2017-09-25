#!/usr/bin/env python
import subprocess
import sys

def writeResults(res):
    outfile = "reports/dnsZT/"+ip_address+"_dnsZT.txt"
    dnsf = open(outfile, "w")
    dnsf.write(ztresults)
    dnsf.close

def main():
    if len(sys.argv) != 2:
        print "Usage: zt-scan.py <ip address>"
        sys.exit(0)

    ip_address = sys.argv[1]
    
    lookupNameCmd = "nmblookup -A "+ip_address+" | grep '<00' | grep -v GROUP | awk '{print $1}'"      
    host = subprocess.check_output(lookupNameCmd, shell=True).strip()
    
    print "[-] Attempting Domain Transfer on " + host

    zoneTransferCmd = "dig @"+host+".thinc.local thinc.local axfr"
    
    try:
        ztresults = subprocess.check_output(zoneTransferCmd, shell=True)
        if "failed" in ztresults:
            print "[-] Zone Transfer failed for " + host
        else:
            print "[-] Zone Transfer successful for " + host + "(" + ip_address + ")"
            writeResults(ztresults)
    except:
        print "[-] Zone Transfer Error", ip_address


main()
