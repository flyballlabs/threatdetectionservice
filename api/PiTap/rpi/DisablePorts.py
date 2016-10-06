'''
This script disables ports
on an rPi network tap
@author: devopsec
'''
import subprocess

def disablePorts():
    
    #disable ssh input / output
    subprocess.call("ufw disable 22", shell=True)
    subprocess.call("iptables -D INPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
    subprocess.call("iptables -D OUTPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -D INPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -D OUTPUT -p ssh --dport 2222 -j ACCEPT", shell=True)
    #disable http input / output
    subprocess.call("ufw disable 80", shell=True)
    subprocess.call("iptables -D INPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    subprocess.call("iptables -D OUTPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -D INPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -D OUTPUT -p tcp --dport 1008 -j ACCEPT", shell=True)
    #disable forward ssh on 2222
    subprocess.call("iptables -D -p ssh --dport 22 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -D -p ssh --dport 22 -j ACCEPT", shell=True)
    #disable forward http on 1008
    subprocess.call("iptables -D -p tcp --dport 80 -j ACCEPT", shell=True)
    subprocess.call("iptables6 -D -p tcp --dport 80 -j ACCEPT", shell=True)
    #stop ssh service
    subprocess.call("service ssh stop", shell=True)
    
return None

