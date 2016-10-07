'''
This script restarts OS
on rPi network tap
@author: devopsec
'''

import subprocess, psutil

def restartPi():
    
    subprocess.call.signal.SIGINT
    subprocess.call("killall -u anon", shell=True)
    subprocess.call("shutdown -r 0", shell=True)

def kill(p_pid):
    process = psutil.Process(p_pid)
    for proc in process.get_children(recursive=True):
        proc.kill()
    process.kill()

p = subprocess.Popen(['gnome-terminal -e bash'], shell=True)
try:
    p.wait(timeout=3)
except subprocess.TimeoutExpired:
    kill(p.pid)
    
    
return None
