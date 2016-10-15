'''
This script checks for cmds from api
and syncs clock with host server
@author: devopsec
'''

import subprocess, requests, sys, json, datetime, socket
sys.path.insert(0, ("/threatdetectionservice/agents/rpi"))
import Ports, Capture, EnableReplay #, RestartPi

## gets args from Ports.check and outputs overall status ##
def portCheck(port80, port1008, port22, port2222):
    if (port80 == True and port1008 == True and port22 == True and port2222 == True):
        check = True
    else:
        check = False
    return check
## end portCheck function

def convTime(tStr):
    t0 = tStr.split(':')
    time0 = datetime.timedelta(hours=int(t0[0]), minutes=int(t0[1]), seconds=int(t0[2]))
    return time0
## end convtime function ##

#if (portCheck(*Ports.func.check()) == False):
#    Ports.func.enable()
    
start=end=cmd=""
r1 = requests.get("http://50.253.243.17:6668/api/picontroller/time")
t = json.loads(r1.text)

#time sync
subprocess.Popen(['timedatectl', 'set-ntp', '0'], bufsize=0,
                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
subprocess.Popen(['timedatectl', 'set-time', t], bufsize=0,
                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
subprocess.Popen(['timedatectl', 'set-ntp', '0'], bufsize=0,
                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

temp = t.split(' ')
t = temp[1]

#variable hostname, ensure hostname is set correctly on device
r2 = requests.get("http://50.253.243.17:6668/api/picontroller/" + socket.gethostname())
cmds = json.loads(r2.text)
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
        ## run if capture is NOT running & within time range & ports open ##
        if Capture.func.isRunning() == False and tnow > tlow and tnow < thigh:
            if (portCheck(*Ports.func.check()) == True):
                Capture.func.enable()
            else:
                Ports.func.enable()
                Capture.func.enable()
            
    elif cmd == 'stop':
        ## stop if capture outside of time range & replay capture ##
        if tnow >= thigh or tnow < tlow:
            if Capture.func.isRunning() == False:
                Ports.func.disable()
                EnableReplay.run()
                Ports.func.enable()
            else:
                Capture.func.kill()
                Ports.func.disable()
                EnableReplay.run()
                Ports.func.enable()
    elif cmd == 'now':
        Capture.func.kill()
        Ports.func.disable()
        EnableReplay.run()
        Ports.func.enable()
        #RestartPi.run()
else:
    ## If no commands are sent then we should fall back to default behavior
    ## which is running a capture between the start and stop time
    if tnow > tlow and tnow < thigh:
        if Capture.func.isRunning() == False:
            Capture.func.enable()
        else:
            Capture.func.disable()
sys.exit(0)