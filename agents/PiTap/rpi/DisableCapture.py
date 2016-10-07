'''
This script disables packet capture
on rPi network tap
@author: devopsec
'''

import subprocess

def disableCapture():
    
    #flush iptables
    
    # IPv6
    ## set default policies to let everything in
    subprocess.call("ip6tables --policy INPUT   ACCEPT", shell=True)
    subprocess.call("ip6tables --policy OUTPUT  ACCEPT", shell=True)
    subprocess.call("ip6tables --policy FORWARD ACCEPT", shell=True)
    ## start fresh
    subprocess.call("ip6tables -Z; # zero counters", shell=True)
    subprocess.call("ip6tables -F; # flush (delete) rules", shell=True)
    subprocess.call("ip6tables -X; # delete all extra chains", shell=True)
    # IPv4
    ## set default policies to let everything in
    subprocess.call("iptables --policy INPUT   ACCEPT", shell=True)
    subprocess.call("iptables --policy OUTPUT  ACCEPT", shell=True)
    subprocess.call("iptables --policy FORWARD ACCEPT", shell=True)
    ## start fresh
    subprocess.call("iptables -Z; # zero counters", shell=True)
    subprocess.call("iptables -F; # flush (delete) rules", shell=True)
    subprocess.call("iptables -X; # delete all extra chains", shell=True)
    
    #enable ssh for debugging
    subprocess.call("iptables -A INPUT -p 22 -j ACCEPT", shell=True)
    subprocess.call("iptables -A OUTPUT -p 22 -j ACCEPT", shell=True)
    subprocess.call("service ssh start", shell=True)
    
return None