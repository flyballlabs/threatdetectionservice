'''
This script checks open ports
on rPi network tap
@author: devopsec
'''

import os, sys, subprocess
from subprocess import *

def checkPorts():
    
    '''
    import socket;
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1',80))
    if result == 0:
        print("Port is open")
    else:
        print("Port is not open")
    
    
    #enable ssh input / output
    out = subprocess.call("ufw status", stderr=subprocess.STDOUT, shell=True)
    if subprocess.Popen("grep -i '6667' $out", shell=True) != None:
        print("found it")
    '''
    
    subprocess.call("iptables -A OUTPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -A INPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -A OUTPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
    #enable http input / output
    subprocess.call("ufw allow 80", shell=True)
    subprocess.call("iptables -A INPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    subprocess.call("iptables -A OUTPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -A INPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -A OUTPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    #forward ssh on 2222
    subprocess.call("iptables -A -p ssh --dport 22 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -A -p ssh --dport 22 -j ACCEPT", shell=True)
    #forward http on 1008
    subprocess.call("iptables -A -p tcp --dport 80 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -A -p tcp --dport 80 -j ACCEPT", shell=True)
    subprocess.call("service ssh start", shell=True)
    
return None