'''
This script enables packet capture
on rPi network tap
@author: devopsec
'''
   
import subprocess, time, sys
sys.path.insert(0, ("/threatdetectionservice/agents/PiTap/"))
from rpi import EnablePorts
from datetime import datetime

pCap = None

#set timer
t = time.time()

#enable ports
EnablePorts()

#dump until killed
while t != 0:
    pCap = subprocess.Popen(["tcpdump", "-n", "-e", "-w", fileOut])
    pCap
