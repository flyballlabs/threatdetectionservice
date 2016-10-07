'''
This script enables packet capture
on rPi network tap
@author: devopsec
'''

import subprocess, time
from datetime import datetime

def enableCapture():
    
    #set timer
    t = time.time()
    
    #accept traffic on any port
    subprocess.call("iptables --policy INPUT   ACCEPT", shell=True)
    subprocess.call("iptables --policy OUTPUT  ACCEPT", shell=True)
    subprocess.call("iptables --policy FORWARD ACCEP", shell=True)
    subprocess.call("ip6tables --policy INPUT   ACCEPT", shell=True)
    subprocess.call("ip6tables --policy OUTPUT  ACCEPT", shell=True)
    subprocess.call("ip6tables --policy FORWARD ACCEPT", shell=True)
    subprocess.call("iptables -I INPUT -j ACCEPT", shell=True)
    subprocess.call("iptables -A INPUT -p any -j ACCEPT", shell=True)
    
    
    dt = datetime.now()
    date = datetime.strftime(dt, '%Y-%m-%d')
    fileOut = "/media/anon/5227-FD18/capture-data/" + date + ".pcap"
    
    #dump until 4pm
    while t < 28800:
        subprocess.call(["tcpdump", "-n", "-e", "-w", fileOut])
        
    #execute replay function 5min after 4pm
    if t >= 28920:
        replay()
    
    #define replay function
    def replay():
        #delete iptables rules
        subprocess.call("iptables -F; # flush (delete) rules", shell=True)
        subprocess.call("ip6tables -F; # flush (delete) rules", shell=True)
        #forward all ports to remote host
        subprocess.call("iptables -A FORWARD portrange 0-65535 -d 50.253.243.17 --dport 6667 -j ACCEPT", shell=True)
        #replay packet captures
        subprocess.call("tcpreplay -q --topspeed --intf1=eno1 fileOut", shell=True)
    return None

return None
