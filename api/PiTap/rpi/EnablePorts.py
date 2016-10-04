'''
This script enables ports
on an rPi network tap
@author: devopsec
'''

import subprocess

def enablePorts():
    
    #enable ssh input / output
    subprocess.call("ufw allow 22", shell=True)
    subprocess.call("iptables -A INPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
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