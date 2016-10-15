'''
This script allows control of capture on rpi network tap
@author: devopsec
'''

import subprocess, time, os, re
from datetime import datetime

'''
@summary: 
This class holds functions for Capturing data
'''
class func:
    pcap = None
    
    def enable():            
    ## get datetime for timestamp ##
        dt = datetime.now()
        date = datetime.strftime(dt, '%Y-%m-%d')
        fileOut = "/capture-data/" + date + ".pcap"
        
        #set timer
        t = time.time()
        
        #dump until killed
        func.pcap = subprocess.Popen(["/usr/sbin/tcpdump -n -e -w "  + fileOut],shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while t != 0:
            func.pcap
    
        return False
    ## end enable function
    
    def kill():
        try:
            func.pcap.terminate()
            return True
        except:
            func.pcap.kill()
            return True
        else:
            return False
    
    ## end killPcap function

    def isRunning():
        ps = subprocess.Popen("ps -eaf | grep /capture-data", shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ps.stdout.readline().decode('ascii')
        print (output)
        try:
            if re.search("pcap",output):
                return True
            else:
                return False
        except:
            return False
    ## end isRunning function ##