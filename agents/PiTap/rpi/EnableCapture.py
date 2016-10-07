'''
This script enables packet capture
on rPi network tap
@author: devopsec
'''

def enableCapture():
    
    from rpi import EnablePorts
    import subprocess, time
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
    
    return None
