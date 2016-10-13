'''
This script enables packet capture on rpi network tap
@author: devopsec
'''
   
import subprocess, time, sys
sys.path.insert(0, ("/threatdetectionservice/agents/rpi/"))
from datetime import datetime

pCap = None

#set timer
t = time.time()

#dump until killed
while t != 0:
    pCap = subprocess.Popen(["tcpdump", "-n", "-e", "-w", fileOut])
    pCap
