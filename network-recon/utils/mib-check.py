#!/usr/bin/python

import subprocess,sys

if len(sys.argv) != 2:
    print "Usage: mib-check.py <ips-file>"
    sys.exit(0)

with open(sys.argv[1]) as f:
    ips = f.readlines()
ips = [x.strip() for x in ips] 

mib = {}
mib['system-processes'] = "1.3.6.1.2.1.25.1.6.0"
mib['running-programs'] = "1.3.6.1.2.1.25.4.2.1.2"
mib['processes-path']   = "1.3.6.1.2.1.25.4.2.1.4"
mib['storage-units']    = "1.3.6.1.2.1.25.2.3.1.4" 
mib['software-name']    = "1.3.6.1.2.1.25.6.3.1.2"
mib['user-accounts']    = "1.3.6.1.4.1.77.1.2.25" 
mib['tcp-local-ports']  = "1.3.6.1.2.1.6.13.1.3"

for ip in ips:
    for k, value in mib.items():
        try: #snmpwalk
            bashCommand = "snmpwalk -c public -v1 " + ip +' ' + value  + " > snmp/"+ip+"-"+k+".txt"
            output = subprocess.check_output(['bash','-c', bashCommand])
        except subprocess.CalledProcessError:
            print "snmpwalk subprocess error", ip, k
    try:#snmpcheck
        bashCommand = "snmp-check "+ip+" -c public > snmp/"+ip+"-snmpcheck.txt"
        output = subprocess.check_output(['bash','-c', bashCommand])
    except subprocess.CalledProcessError:
        print "snmpcheck subprocess error", ip
    print "ip: ", ip
