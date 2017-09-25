#!/bin/bash

# reset all counters and ip tables rules
iptables -Z && iptables -F
# measure incoming traffic to 192.168.1.89
iptables -I INPUT 1 -s 192.168.1.89 -j ACCEPT
#measure outgoing traffic to 192.168.1.89
iptables -I OUTPUT 1 -d 192.168.1.89 -j ACCEPT
