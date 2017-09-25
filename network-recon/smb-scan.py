#!/usr/bin/env python
import sys, subprocess


def nmapScriptsScan( ip, port):
    print "[-] Starting nmap smb script scan for " + ip + ":" + port
    nmapCmd = "nmap -sV -Pn -v -p "+port+" --script='(smb*) and not (brute or broadcast or dos or external or fuzzer)' --script-args=unsafe=1 -oN reports/smb/"+ip+"_"+port+"_nmap "+ip+ " >> reports/smb/"+ip+"_"+port+"_nmapOut.txt"
    subprocess.check_output(nmapCmd, shell=True)
    print "[-] Nmap smb script scan completed for " + ip + ":" + port

def usersEnum(ip, port):
    print "[-] Starting SAMRDUMP Users Enum on " + ip + ":" + port
    samrdump = "/usr/share/doc/python-impacket/examples/samrdump.py"
    nbtCmd = samrdump+" "+ip
    results = subprocess.check_output(nbtCmd, shell=True)
    if ("Connection refused" not in results) and ("Connect error" not in results) and ("Connection reset" not in results):
        print "[*] SAMRDUMP has found something on "+ip+":"+port
        fdesc = open("reports/smb/"+ip+"_"+port+"_samrdump.txt","w")
        fdesc.write("User accounts/domains on " + ip+ ":"+port+"\n")
        lines = results.split("\n")
        for line in lines:
                if ("Found" in line) or (" . " in line):
		    fdesc.write(" [*] " + line + "\n")
	fdesc.close()
    print "[-] Completed SAMRDUMP  Users Enum on " + ip + ":" + port

def nbtScan(ip, port):
    print "[-] Starting ntbscan for " + ip + ":" + port
    nbtCmd = "nbtscan -r -v -h "+ip+" >> reports/smb/"+ip+"_"+port+"_ntbscan.txt"
    subprocess.check_output(nbtCmd, shell=True)
    print "[-] Completed ntbscan for " + ip + ":" + port

def smbEnum (ip, port):
    print "[-] Starting enum4linux scan for " + ip + ":" + port
    try:
        enumCmd = "enum4linux -a -M -v "+ip+" >> reports/smb/"+ip+"_"+port+"_enum4linux.txt"
        subprocess.check_output(enumCmd , shell=True)
    except:
        print "[-] Error during enum4linux scan for " + ip + ":" + port
    print "[-] Completed enum4linux scan for " + ip + ":" + port

def main():
    if len(sys.argv) != 3:
        print "Usage: smbscan.py <ip> <port>"
        sys.exit(0)
    ip = sys.argv[1]
    port = sys.argv[2]
    nmapScriptsScan( ip, port)
    nbtScan(ip, port)
    smbEnum (ip, port)
    usersEnum(ip, port)

main()
