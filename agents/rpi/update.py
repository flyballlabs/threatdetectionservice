'''
This script checks for cmds from api
and syncs clock with host server
@author: devopsec
'''

import subprocess, requests, sys, json, datetime, socket, platform
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

## get the name of the linux distribution
def getLinuxDistro():
    try:    
      linuxDistroInfo = platform.linux_distribution()
      return str.lower(linuxDistroInfo[0])
    except:
      return "n/a"
## end getLinuxDistro ##

#if (portCheck(*Ports.func.check()) == False):
#    Ports.func.enable()
    
start=end=cmd=""
r1 = requests.get("http://50.253.243.17:6668/api/picontroller/time")
t = json.loads(r1.text)

distro = getLinuxDistro()

#Update the time if the agent is running on Ubuntu, which is the OS that we are running on the pi
#The timedatactl command only workson Ubuntu.  So, we don't want to run it on other OS's that we 
#we might use for development

if distro == "ubuntu":
    subprocess.Popen(['timedatectl', 'set-ntp', '0'], bufsize=0)
    subprocess.Popen(['timedatectl', 'set-time', t], bufsize=0)
    subprocess.Popen(['timedatectl', 'set-ntp', '0'], bufsize=0)

temp = t.split(' ')
t = temp[1]

#We need to obtain control information for the agent.  Each agent is identified by a device id 
#The device id is the hostname of the device or it can be overridden with the [deviceid] parameter
#on the command line

if len(sys.argv) > 1:
    deviceID = sys.argv[1]
else:
    deviceID = socket.gethostname()

r2 = requests.get("http://50.253.243.17:6668/api/picontroller/" + deviceID)

#Check if the request was not successfull.
if r2.status_code > 400:
    print("Could not obtain control information for" + deviceID + ".\nYou can force a deviceID by adding it to the commmand line as show below: \nupdate.py [deviceId]")
    sys.exit(0)

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
        if Capture.func.pcap.pid == None:
            if tnow > tlow and tnow < thigh:
                if (portCheck(*Ports.func.check()) == True):
                    Capture.func.enable()
                else:
                    Ports.func.enable()
                    Capture.func.enable()
            
    elif cmd == 'stop':
        ## stop if capture outside of time range & replay capture ##
        if tnow >= thigh or tnow < tlow:
            if Capture.func.pcap.pid == None:
                Ports.func.disable()
                EnableReplay.run()
                Ports.func.enable()
            else:
                Capture.func.disable()
                Ports.func.disable()
                EnableReplay.run()
                Ports.func.enable()
    elif cmd == 'now':
        Capture.func.disable()
        Ports.func.disable()
        EnableReplay.run()
        Ports.func.enable()
        #RestartPi.run()
else:
	## If no commands are sent then we should fall back to default behavior
        ## which is running a captures between the start and stop time
	if tnow > tlow and tnow < thigh:
		if Capture.func.isRunning()  == False:
			Capture.func.enable()
        
	else:
           Capture.func.disable()
sys.exit(0)

