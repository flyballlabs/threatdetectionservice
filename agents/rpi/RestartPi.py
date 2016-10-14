'''
This script restarts OS on rPi network tap
@author: devopsec
'''
import subprocess, os, sys
sys.path.insert(0, ("/threatdetectionservice/agents/rpi"))
from time import sleep

def run():
    from signal import *
    
    subprocess.run("signal.SIGINT", shell=True)
    
    def kill(p_pid):
            process = psutil.Process(p_pid)
            for proc in process.get_children(recursive=True):
                proc.kill()
                process.kill()
    ## end kill function ##
    
    try:
        import Capture
        import psutil
        kill(Capture.func.pcap.pid)
    except:
        pass
    
    p = subprocess.Popen(['gnome-terminal -e bash'], shell=True)
    try:
        p.wait(timeout=3)
    except p.TimeoutExpired:
        kill(p.pid)
        
    subprocess.run("killall -u anon", shell=True)
        
    try:
        sys.exit(0)
        sleep(5)
    except:
        os._exit(0)
    
    subprocess.run("shutdown -r 0", shell=True)
## end run function ##