'''
This script allows control of capture on rpi network tap
@author: devopsec
'''

import subprocess, time, sys, os
sys.path.insert(0, ("/threatdetectionservice/agents/"))
from datetime import datetime

'''
@summary: 
This class holds functions for Capture
'''
class func():
    pcap = None
    
    def enable():            
        ## get datetime for timestamp ##
        dt = datetime.now()
        date = datetime.strftime(dt, '%Y-%m-%d')
        fileOut = "/capture-data/" + date + ".pcap"
        
        #set timer
        t = time.time()
        
        #dump until killed
        func.pcap = subprocess.Popen(["tcpdump", "-n", "-e", "-w", fileOut])
        while t != 0:
            func.pcap
    ## end run function
    
    #def getpcap(self):
    #   return self.pcap
    ## end getpcap
    
    def kill():
        try:
            func.pcap.send_signal(SIGINT)
        except:
            func.pcap.kill()
        else:
            return 1
    ## end killPcap function
