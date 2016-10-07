'''
This script checks open ports
on rPi network tap
@author: devopsec
'''

def checkPorts():
    
    import socket#, subprocess
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    check = sock.connect_ex(('10.10.10.101',80))
    if check == 0:
        result = True
    else:
        result = False
    
    check = sock.connect_ex(('10.10.10.101',22))
    if check == 0:
        result = True
    else:
        result = False
    
    #enable ssh input / output
    #out = subprocess.Popen("ufw status", stderr=subprocess.PIPE, shell=True)
    #if subprocess.Popen('grep', '-i', '6667', out, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) != None:
    #    print("found it")
    
    return result