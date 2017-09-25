#!/usr/bin/python

import sys, os, subprocess

def nmapScriptsScan( ip, port, serv):
    print "[-] Starting nmap web script scan for " + ip + ":" + port
    nmapCmd = "nmap -sV -Pn -v -p "+port+" --script='(http* or ssl*) and not (broadcast or dos or external or http-slowloris* or fuzzer)' -oN reports/web-serv/"+ip+"_"+port+"_"+serv+"_nmap "+ip+ " >> reports/web-serv/"+ip+"_"+port+"_"+serv+"_nmapOutput.txt"
    subprocess.check_output(nmapCmd, shell=True)
    print "[-] Nmap web script scan completed for " + ip + ":" + port

def niktoScan(ip, port, serv):
    print "[-] Starting Nikto Scan on " + ip + ":" + port
    niktoCmd = "nikto -host "+ip+" -p "+port+" -o reports/web-serv/"+ip+"_"+port+"_"+serv+"_nikto.txt -C all"
    subprocess.check_output(niktoCmd, shell=True)
    print "[-] Completed Nikto Scan on " + ip + ":" + port
    
def dirBust(url, name, port):
    url = str(sys.argv[1])
    name = str(sys.argv[2])
    folders = ["/usr/share/dirb/wordlists", "/usr/share/dirb/wordlists/vulns"]
    found = []
    print "[-] Starting dirb scan for " + url + ":" + port
    for folder in folders:
        for filename in os.listdir(folder):
            outFile = " -o " + "reports/web-serv/" + url + "_" + port + "_"+name+"_dirb_" + filename
            DIRBSCAN = "dirb "+url+" "+folder+"/"+filename+" "+outFile+" -S -r -w"
            try:
                results = subprocess.check_output(DIRBSCAN, shell=True)
                results_list = results.split("\n")
                for line in results_list:
                    if "+" in line:
                        if line not in found:
                            found.append(line)
            except:
                pass
    try:
        if found[0] != "":
            print "[-] Dirb has found something for "+ url+":"+port
            outfile = "reports/web-serv/"+ip+"_"+port+"_"+name+"_dirbItems.txt"
            dirbf = open(outfile, "w")
            for item in found:
                dirbf.write(item+"\n")
            dirbf.close
    except:
        print "[-] Dirb didn't find items for "+ url+":"+port

def main():
    if len(sys.argv) != 4:
        print "Passed: ",sys.argv
        print "Usage: web-scan.py <targetUrl> <port> <serviceName>"
        sys.exit(0)

    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    serv = str(sys.argv[3])
    
    nmapScriptsScan( ip, port, serv)
    dirBust( ip, serv, port)
    #niktoScan( ip, port, serv)

main()
    
