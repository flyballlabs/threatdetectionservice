'''
This script replays pcap capture over the net to host server
Make sure to re-enable ports after
@author: devopsec
'''

def iptablesFLUSH():
    subprocess.run("iptables -Z", shell=True)# zero counters
    subprocess.run("iptables -F", shell=True)# flush (delete) rules
    subprocess.run("iptables -X", shell=True)# delete all extra chains
    subprocess.run("ip6tables -Z", shell=True)# zero counters
    subprocess.run("ip6tables -F", shell=True)# flush (delete) rules
    subprocess.run("ip6tables -X", shell=True)# delete all extra chains

#get datetime for timestamp
dt = datetime.now()
date = datetime.strftime(dt, '%Y-%m-%d_%H%M')
fileOut = "/capture-data/" + date + ".pcap"

#delete iptables rules
iptablesFLUSH()

## set policies to let everything in
subprocess.run("iptables --policy INPUT   ACCEPT", shell=True)
subprocess.run("iptables --policy OUTPUT  ACCEPT", shell=True)
subprocess.run("iptables --policy FORWARD ACCEPT", shell=True)
subprocess.run("ip6tables --policy INPUT   ACCEPT", shell=True)
subprocess.run("ip6tables --policy OUTPUT  ACCEPT", shell=True)
subprocess.run("ip6tables --policy FORWARD ACCEPT", shell=True)

#enable all traffic in ufw
subprocess.run("ufw allow incoming", shell=True)
subprocess.run("ufw allow outgoing", shell=True)
subprocess.run("ufw allow 0:65535/tcp", shell=True)

#forward all ports to remote host
subprocess.run("iptables -A FORWARD portrange 0-65535 -d 50.253.243.17 --dport 6667 -j ACCEPT", shell=True)

#replay packet captures
subprocess.Popen(["tcpreplay", "-q", "--topspeed", "--intf1=eno1", fileOut], shell=True)

#delete ufw rules
subprocess.run("ufw delete allow incoming", shell=True)
subprocess.run("ufw delete allow outgoing", shell=True)
subprocess.run("ufw delete allow 0:65535/tcp", shell=True)

#delete added iptables rules
iptablesFLUSH()
