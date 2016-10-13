'''
This script disables packet capture on rpi network tap
@author: devopsec
'''

import subprocess, sys
sys.path.insert(0, ("/threatdetectionservice/agents/rpi/"))
from rpi import EnableCapture

#send sigint
subprocess.run("signal.SIGINT", shell=True)
try:
    os.kill(pid, EnableCapture.pCap.pid)
except:
    pass
    
 