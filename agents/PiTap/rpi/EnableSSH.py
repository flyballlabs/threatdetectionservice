'''
This script enables SSH for debugging
on an rPi network tap
@author: devopsec
'''

import subprocess

def enableSSH():
    
    #enable ssh for debugging
    subprocess.call("ufw allow 22", shell=True)
    subprocess.call("iptables -A INPUT -p 22 -j ACCEPT", shell=True)
    subprocess.call("iptables -A OUTPUT -p 22 -j ACCEPT", shell=True)
    subprocess.call("service ssh start", shell=True)
    
return None