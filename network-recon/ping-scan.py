#!/usr/bin/python

import threading
import Queue
import subprocess
import sys

if len(sys.argv) != 2:
    print "Usage: ping-scan.py <ip address>"
    sys.exit(0)

#IP = "192.168.1."
IP = sys.argv[1].strip()
IPs = {}
queue = Queue.Queue()

def pingIP(i, q):
    while True:
        ip = q.get()
        ret = subprocess.call("ping -c 1 %s" % ip, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
	if ret == 0:
            IPs[ip] = True
        q.task_done()

def sort_key(item):
    return int(item[0].split('.')[-1])

def main():
    for i in range(1,255):
        address = IP + str(i)
        IPs[address] = False
        worker =  threading.Thread(target=pingIP, args=(i, queue))
        worker.setDaemon(True)
        worker.start()
    for k, v in IPs.items():
        queue.put(k)
    queue.join()

    fdesc = open("reports/pingIPs.txt","w")
    for ip, alive in sorted(IPs.items(), key=sort_key):
        if alive:
            print ip
            fdesc.write(ip + "\n")
    fdesc.close()

main()
