#!/usr/bin/env python
import subprocess, sys

def nmapScriptsScan( ip, port):
    print "[-] Starting nmap snmp script scan for " + ip + ":" + port
    nmapCmd = "nmap -sV -Pn -v -p "+port+" --script=snmp* -oN reports/snmp/"+ip+"_"+port+"_nmap "+ip+ " >> reports/snmp/"+ip+"_"+port+"_nmapOut.txt"
    subprocess.check_output(nmapCmd, shell=True)
    print "[-] Completed nmap snmp script scan for " + ip + ":" + port

def onesixtyoneScan(ip, port):
    print "[-] Starting OneSixtyOne snmp scan for " + ip + ":" + port
    cmdOSO="onesixtyone -c wordlists/community.txt "+ip+" >> reports/snmp/"+ip+"_"+port+"_OneSixtyOne.txt"
    subprocess.check_output(oneSixtyOneSCAN, shell=True)
    print "[-] Completed OneSixtyOne snmp scan for " + ip + ":" + port

def snmpWalkCheck(ip, port):
    options=['1.3.6.1.2.1.25.1.6.0', '1.3.6.1.2.1.25.4.2.1.2', '1.3.6.1.2.1.25.4.2.1.4', '1.3.6.1.2.1.25.2.3.1.4', '1.3.6.1.2.1.25.6.3.1.2', '1.3.6.1.4.1.77.1.2.25', '1.3.6.1.2.1.6.13.1.3']
    print "[-] Starting snmpwalk scan for " + ip + ":" + port
    for opt in options:
        try:
            snmpWalkCmd="snmpwalk -c public -v1 "+ip+" "+opt+" >> reports/snmp/"+ip+"_"+port+"_snmpwalk.txt"
            subprocess.check_output(snmpWalkCmd, shell=True)
        except:
            pass
    print "[-] Completed snmpwalk scan for " + ip + ":" + port
    print "[-] Starting snmpcheck scan for " + ip + ":" + port
    try:
        snmpCheckSCAN="snmpcheck -t "+ip+" >> reports/snmp/"+ip+"_"+port+"_snmpcheck.txt"
        subprocess.check_output(snmpCheckSCAN, shell=True)
    except:
        pass
    print "[-] Completed snmpcheck scan for " + ip + ":" + port
  
def main(ip, port):
    if len(sys.argv) != 3:
        print "Usage: snmp-scan.py <ip> <port>"
        sys.exit(0)
    ip = sys.argv[1]
    port = sys.argv[2]
    nmapScriptsScan(ip, port)
    onesixtyoneScan(ip, port)
    snmpWalkCheck(ip, port)
    

main()
