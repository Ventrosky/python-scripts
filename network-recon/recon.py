#!/usr/bin/env python

import sys
import getopt
import subprocess
import threading
import Queue
import re
import multiprocessing

#global variables
targetsIPs          = "reports/alive.txt"
nmapReportsDir      = "/root/scripts/recon/reports/nmap/"
ping_sweep          = ""
singleIP            = ""
queue               = Queue.Queue()
scanUDP             = True

def usage():
    print "Recon Scan"
    print
    print "Usage: recon.py "
    print "-h --help                    - list usage options"
    print "-t --targets=file_ips        - specify file for target list"
    print "-p --ping-sweep=subnet_ip    - ping-sweep to generate targets list"
    print "-s --single=target_ip        - execute on single target ip"
    print "-u --skip-udp                - skip UDP scan"
    print
    print
    print "Examples: "
    print "recon.py -u "
    print "recon.py -t reports/targets.txt "
    print "recon.py -p 192.168.1. "
    print "recon.py -s 192.168.1.89 "
    sys.exit(0)

def getTargets():
    fdesc = open(targetsIPs,"r")
    targets = []
    for line in fdesc.readlines():
        targets.append(line.strip())
    fdesc.close()
    return targets

def startNewProcess( method, arguments):
    p = multiprocessing.Process(target=method, args=(arguments,))	
    #p.start()
    return p

def pingSweep():
    print "[-] Executing Ping Sweep on", ping_sweep
    SCRIPT = "./ping-scan.py %s" % (ping_sweep)       
    subprocess.call(SCRIPT, shell=True)
    return

def nmapGenericScan(target):
    print "[-] Executing TCP/UDP scan on", target
    optionTCP = 'nmap -v -p- -Pn -A -sC -sS -T 4 -oG '+ nmapReportsDir + target + "_TCP_nmap " + target +" >> "+ nmapReportsDir + target + "_TCP_nmap_output" 
    optionUDP = 'nmap -v --top-ports 200 -Pn -A -sC -sU -T 4 -oG ' + nmapReportsDir + target + '_UDP_nmap ' + target +" >> "+ nmapReportsDir + target + "_UDP_nmap_output" 
    resultTCP = subprocess.check_output(optionTCP, shell= True)
    TCP_list = resultTCP.split("\n")
    UDP_list = []
    if scanUDP:
        resultUDP = subprocess.check_output(optionUDP, shell= True)
        UDP_list = resultTCP.split("\n")
    return (TCP_list, UDP_list)

def resultsDict(scan_res, servDict):
    for line in TEST_RESULT:
        ports = []
        match = re.search('^(\d+)/\w\w\w\s+open\s+([\w.-]+)', line)
        if match:
            port = match.group(1)
            serv = match.group(2)
            if serv in servDict:
                ports = servDict[serv]
            if port not in ports:
                ports.append(port)
            servDict[serv] = ports
    return servDict

def dnsEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] DNS Recon on " + ip + ":" + port
    script = "./zt-scan.py "+ ip        
    subprocess.call(script, shell=True)
    return

def httpEnum(args):
    ip = args[0]
    port = args[1]
    serv = args[2]
    print "[-] Web service on " + ip + ":" + port
    script = "./web-scan.py "+ ip+" "+ port+" "+ serv        
    subprocess.call(script, shell=True)
    return

def sshEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] Detected SSH on " + ip + ":" + port
    script = "./ssh-scan.py "+ ip+" "+ port       
    subprocess.call(script, shell=True)
    return

def ftpEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] Detected FTP on " + ip + ":" + port
    script = "./ftp-scan.py "+ ip +" "+ port           
    subprocess.call(script, shell=True)
    return

def smtpEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] Detected smtp on " + ip + ":" + port
    script = "./smtp-scan.py "+ ip +" "+ port           
    subprocess.call(script, shell=True)
    return

def snmpEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] Detected snmp on " + ip + ":" + port
    script = "./snmp-scan.py "+ ip +" "+ port           
    subprocess.call(script, shell=True)
    return

def smbEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] Detected smb on " + ip + ":" + port
    script = "./smb-scan.py "+ ip +" "+ port           
    subprocess.call(script, shell=True)
    return

def rdpEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] Detected rdp on " + ip + ":" + port
    script = "./rdp-scan.py "+ ip +" "+ port           
    subprocess.call(script, shell=True)
    return

def sqlEnum(args):
    ip = args[0]
    port = args[1]
    print "[-] Detected ms-sql on " + ip + ":" + port
    script = "./sql-scan.py "+ ip +" "+ port           
    subprocess.call(script, shell=True)
    return


def moreEnum(servDict, ip):
   print "[-] Enumerate, enumerate, enumerate.", ip
   jobs = []
   for serv, ports in servDict.items():
      if 'ssl' in serv or 'http' in serv:
         for port in ports:
            p = startNewProcess(httpEnum, [ip, port, serv])
            jobs.append(p)
            p.start()
      elif "ssh" in serv:  
         for port in ports:
            p = startNewProcess(sshEnum, [ip, port])
            jobs.append(p)
            p.start()
      elif ("domain" in serv) or ("dns" in serv): 
         for port in ports:
            p = startNewProcess(dnsEnum,[ip, port])
            jobs.append(p)
            p.start()
      elif ("ftp" in serv):  
         for port in ports:
            p = startNewProcess(ftpEnum, [ip, port])
            jobs.append(p)
            p.start()
      elif "smtp" in serv: 
         for port in ports:
            p = startNewProcess(smtpEnum, [ip, port])
            jobs.append(p)
            p.start()
      elif "snmp" in serv: 
         for port in ports:
            p = startNewProcess(snmpEnum, [ip, port])
            jobs.append(p)
            p.start()
      elif ("smb" in serv) or ("microsoft-ds" in serv):   
         for port in ports:
            p = startNewProcess(smbEnum, [ip, port])
            jobs.append(p)
            p.start()
      elif ('ms-sql'in serv) or ('msSql'in serv): 
         for port in ports:
            p = startNewProcess(sqlEnum, [ip, port])
            jobs.append(p)
            p.start()
      elif serv == 'rdp' or serv == ' microsoft-rdp' or serv == 'ms-wbt-server' or serv == 'ms-term-serv':
         for port in ports:  
            p = startNewProcess(rdpEnum, ip_address, port)
            jobs.append(p)
            p.start()
      else:
          print "[-] No module found for", serv
   return

class ReconWorker(threading.Thread) : 

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            target = self.queue.get()
            print "[-] Starting TCP/UDP scans for target: %s"%target
            resTCP, resUDP = nmapGenericScan(target)                   
            servDict = resultsDict(resUDP, resultsDict(resTCP, {}))
            moreEnum(servDict, target)
            print "[-] Finished TCP/UDP scans for target: %s"%target
            self.queue.task_done()

def createWorkers(targets):
    for ip in targets:
        print "[-] Creating ReconWorker: %s"%ip
        worker = ReconWorker(queue)
        worker.setDaemon(True)
        worker.start()
        print "[-] ReconWorker %s Created!"%ip
    for ip in targets:
        queue.put(ip)
    queue.join()
    print "[-] All tasks are over!"
 
def main():
    global targetsIPs
    global ping_sweep
    global singleIP
    global queue
    global scanUDP
    
    if not len(sys.argv[1:]):
        usage()
        
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'us:t:p:h', ['skip-udp','single=', 'targets=', 'ping-sweep=', 'help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-t', '--targets'):
            targetsIPs = arg
        elif opt in ('-p', '--ping-sweep'):
            ping_sweep = arg
        elif opt in ('-s', '--single'):
            singleIP = arg
        elif opt in ('-u', '--skip-udp'):
            scanUDP = False
        else:
            usage()
            sys.exit(2)

    if ping_sweep != "":
        pingSweep()
        targetsIPs = "reports/pingIPs.txt"

    targets = []  
    if singleIP == "":
        targets = getTargets()
    else:
        targets.append(singleIP)

    print "+-+-+-+-+-+ +-+-+-+-+   +-+-+-+-+"
    print "|R|e|c|o|n| |S|c|a|n|   |v|1|.|0|"
    print "+-+-+-+-+-+ +-+-+-+-+   +-+-+-+-+"
    print
    print targets
    print "Press Enter to confirm targets"
    raw_input()
    createWorkers(targets)

main()


