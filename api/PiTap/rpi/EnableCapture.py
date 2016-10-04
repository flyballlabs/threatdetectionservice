'''
This script enables packet capture
on rPi network tap
@author: devopsec
'''
from rpi import EnablePorts
import subprocess, time
from datetime import datetime

def enableCapture():
    
    #set timer
    t = time.time()
    
    dt = datetime.now()
    date = datetime.strftime(dt, '%Y-%m-%d')
    fileOut = "/media/anon/5227-FD18/capture-data/" + date + ".pcap"
    
    #enable ports
    EnablePorts()
    
    #dump until 4pm
    while t < 28800:
        subprocess.call(["tcpdump", "-n", "-e", "-w", fileOut])
        
    #execute replay function 5min after 4pm
    if t >= 28920:
        replay()
    
    #define replay function
    def replay():
        #delete iptables rules
        subprocess.call("iptables -F", shell=True)
        subprocess.call("ip6tables -F", shell=True)
        #forward all ports to remote host
        subprocess.call("iptables -A FORWARD portrange 0-65535 -d 50.253.243.17 --dport 6667 -j ACCEPT", shell=True)
        #replay packet captures
        subprocess.call("tcpreplay -q --topspeed --intf1=eno1 fileOut", shell=True)
    return None
    
    #re-enable ports
    EnablePorts()
return None
