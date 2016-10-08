'''
This script checks for cmds from api
and syncs clock with host server
@author: devopsec
'''

import subprocess, requests, sys
sys.path.insert(0, ("/threatdetectionservice/agents/PiTap/"))
import datetime, socket
from rpi import EnableCapture

start, end, cmd = ""
#chk = False
r1 = requests.get("http://10.10.10.154:6668/api/picontroller/time")
t = r1.text
subprocess.Popen('timedatectl', 'set-time', t)

#variable hostname, ensure hostname is set correctly on device
r2 = requests.get("http://10.10.10.154:6668/api/picontroller/" + socket.gethostname())
cmds = r2.text
if cmds['start'] != "":
    start = cmds['start']
if cmds['end'] != "":
    end = cmds['end']
tlow = convTime(start)
thigh = convTime(end)
tnow = convTime(t)

if cmds['cmd'] != "":
    cmd = cmds['cmd']
    if cmd == 'start':
        if EnableCapture.pCap.pid == None:
            if tnow > tlow & tnow < thigh:
                EnableCapture()
            
            
    elif cmd == 'stop':
        if tnow >= thigh:
            from rpi import EnableReplay, EnablePorts, DisableCapture, DisablePorts
            if EnableCapture.pCap.pid == None:
                DisablePorts()
                EnableReplay()
                EnablePorts()
            else:
                from rpi import DisableCapture, DisablePorts
                DisablePorts()
                DisableCapture()
                EnableReplay()
                EnablePorts()
    elif cmd == 'now':
        from rpi import RestartPi
        RestartPi()

#define convtime func
def convTime(tStr):
    t0 = tStr
    t0 = t0.split(' ')
    t0 = t0[1].split(':')
    time0 = datetime.timedelta(hours=int(t0[0]), minutes=int(t0[1]), seconds=int(t0[2]))
    return time0  

sys.exit(0)

        


        
        
    