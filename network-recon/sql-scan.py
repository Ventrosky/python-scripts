#!/usr/bin/env python

import sys, os, subprocess

def nmapScriptsScan(ip, port):
    print "[-] Starting nmap ms-sql script scan for " + ip + ":" + port
    nmapCmd = "nmap -sV -Pn -v -p "+port+" --script=ms-sql* -oN reports/sql/"+ip+"_"+port+"_nmap "+ip+ " >> reports/sql/"+ip+"_"+port+"_nmapOutput.txt"
    subprocess.check_output(nmapCmd, shell=True)
    print "[-] Completed nmap ms-sql script scan for " + ip + ":" + port
    
def hydraScan(ip, port):
    print "[-] Starting ms-sql against " + ip + ":" + port
    hydraCmd = "hydra -L wordlists/users.txt -P wordlists/passwords.txt  -f -e n -o reports/sql/"+ip+"_"+port+"_ncrack.txt -u "+ip+" -s "+port + "mssql"
    try:
            results = subprocess.check_output(hydraCmd, shell=True)
            resultarr = results.split("\n")
            for result in resultarr:
                if "login:" in result:
                    print "[*] Valid ms-sql credentials found: " + result
                    resultList=result.split()
                    self.username=resultList[4]
                    if resultList[6]:
                        self.password=resultList[6]
                    else:
                        self.password=''
    except:
        print "[-] No valid ms-sql credentials found"
    print "[-] Completed hydra ms-sql against " + ip + ":" + port


def main():
    if len(sys.argv) != 3:
        print "Passed: ",sys.argv
        print "Usage: sql-scan.py <ip> <port> "
        sys.exit(0)
    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    nmapScriptsScan( ip, port)
    hydraScan( ip, port)

main()
