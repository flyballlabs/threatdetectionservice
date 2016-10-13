'''
This script checks open ports
on rPi network tap
@author: devopsec
'''

import socket

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    ## check HTTP ports ##
    check = sock.connect_ex(('10.113.145.149',80))
    if check == 0:
        port80 = True
    else:
        port80 = False
        
    check = sock.connect_ex(('10.113.145.149',1008))
    if check == 0:
        port1008 = True
    else:
        port1008 = False
    
    ## check SSH ports ##
    check = sock.connect_ex(('10.113.145.149',22))
    if check == 0:
        port22 = True
    else:
        port22 = False
    
    check = sock.connect_ex(('10.113.145.149',2222))
    if check == 0:
        port2222 = True
    else:
        port2222 = False
    
    sock.close()
    return (port80, port1008, port22, port2222)

## alternate method ##
#import subprocess
#out = subprocess.Popen("ufw status", stderr=subprocess.PIPE, shell=True)
#if subprocess.Popen('grep', '-i', '6667', out, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) != None:
#    print("found it")
