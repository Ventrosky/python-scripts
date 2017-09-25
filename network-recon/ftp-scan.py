#!/usr/bin/env python
import subprocess, sys, os


def nmapScriptsScan( ip, port):
    print "[-] Starting nmap FTP script scan for " + ip + ":" + port
    nmapCmd = "nmap -sV -Pn -v -p "+port+" --script=ftp* -oN reports/ftp/"+ip+"_"+port+"_nmap "+ip+ " >> reports/ftp/"+ip+"_"+port+"_nmapOutput.txt"
    subprocess.check_output(nmapCmd, shell=True)
    print "[-] Nmap FTP script scan completed for " + ip + ":" + port

def hydraScan(ip, port):
    print "[-] Starting hydra ftp scan against :" + ip  + ":" + port
    hydraCmd = "hydra -L wordlists/users.txt -P wordlists/passwords.txt -f -o reports/ssh/"+ip+"_hydra.txt -u "+ip+" -s "+port+" ftp"
    results = subprocess.check_output(hydraCmd, shell=True)
    try:
        results = subprocess.check_output(hydraCmd , shell=True)
        result_list = results.split("\n")
        for result in result_list:
            if "login:" in result:
                print "[*] Found valid ssh credentials for "+ip+":"+port+"\n" + result  
    except:
        print "[*] Not found valid ssh credentials"


def main():
    if len(sys.argv) != 3:
        print "Usage: ftp-scan.py <ip> <port>"
        sys.exit(0)
    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    nmapScriptsScan( ip, port)
    hydraScan(ip, port)

    
main()
