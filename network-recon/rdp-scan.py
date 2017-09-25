#!/usr/bin/env python

import sys, os, subprocess

def nmapScriptsScan(ip, port):
    print "[-] Starting nmap rdp script scan for " + ip + ":" + port
    nmapCmd = "nmap -sV -Pn -vv -p "+port+" --script=rdp* -oN reports/rdp/"+ip+"_"+port+"_nmap "+ip+ " >> reports/rdp/"+ip+"_"+port+"_nmapOutput.txt"
    subprocess.check_output(nmaCmd, shell=True)
    print "[-] Completed nmap rdp script scan for " + ip + ":" + port
    
def ncrackScan(ip, port):
    print "[-] Starting ncrack rdp scan against " + ip + ":" + port
    ncrackCmd = "ncrack -U wordlists/users.txt -P wordlists/passwords.txt -f -oN reports/rdp/"+ip+"_"+port+"_ncrack.txt "+ip+":"+port
    try:
        results = subprocess.check_output(ncrackCmd, shell=True)
        resultlist = results.split("\n")
        found=""+ip+" "+port+"/tcp rdp:"
        for result in resultlist:
            if found in result:
                print "[*] Valid rdp credentials found: " + result 
    except:
        print "[-] No valid rdp credentials found"
    print "[-] Completed ncrack rdp scan against " + ip + ":" + port


def main():
    if len(sys.argv) != 3:
        print "Passed: ",sys.argv
        print "Usage: rdp-scan.py <ip> <port> "
        sys.exit(0)
    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    nmapScriptsScan( ip, port)
    ncrackScan( ip, port)

main()
    
