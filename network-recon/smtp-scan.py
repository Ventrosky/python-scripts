#!/usr/bin/env python
import socket, sys, subprocess

def readUsersList():
    fdesc = open("wordlists/users.txt","r")
    users = []
    for line in fdesc.readlines():
        users.append(line.strip())
    fdesc.close()
    return users

def writeUsersEnum(ip, port, resoults):
    fdesc = open("reports/smtp/"+ip+"_"+port+"_UsersEnum.txt","w")
    fdesc.write(resoults)
    fdesc.close()

def nmapScriptsScan( ip, port):
    print "[-] Starting nmap smtp script scan for " + ip + ":" + port
    nmapCmd = "nmap -sV -Pn -v -p "+port+" --script=smtp* -oN reports/smtp/"+ip+"_"+port+"_nmap "+ip+ " >> reports/smtp/"+ip+"_"+port+"_nmapOut.txt"
    subprocess.check_output(nmapCmd, shell=True)
    print "[-] Nmap smtp script scan completed for " + ip + ":" + port

def usersEnum( ip, port, users):
        print "[-] Starting brute force user enum for " + ip + ":" + port
        result=""
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect=s.connect((ip,int(port)))
        banner=s.recv(1024)
        result+=banner +"\n"
        for user in users:
            s.send('VRFY ' + user + '\r\n')
            response=s.recv(1024)
            if "250 " in response[:4]:
                result+=response
        s.close()
        writeUsersEnum(ip, port, result)
        print "[-] Completed brute force user enum for " + ip + ":" + port


def main():
    if len(sys.argv) != 3:
        print "Usage: smtp-scan.py <ip> <port>"
        sys.exit(0)
    ip = sys.argv[1]
    port = sys.argv[2]
    nmapScriptsScan(ip, port)
    users = readUsersList()
    usersEnum(ip, port, users)

main()
