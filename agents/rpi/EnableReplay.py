'''
This script replays pcap capture over the net to host server
Make sure to re-enable ports after
@author: devopsec
'''
import subprocess, sys
from datetime import datetime

def run():
    
    def iptablesFLUSH():
        subprocess.run("iptables -Z", shell=True)# zero counters
        subprocess.run("iptables -F", shell=True)# flush (delete) rules
        subprocess.run("iptables -X", shell=True)# delete all extra chains
        subprocess.run("ip6tables -Z", shell=True)# zero counters
        subprocess.run("ip6tables -F", shell=True)# flush (delete) rules
        subprocess.run("ip6tables -X", shell=True)# delete all extra chains
    
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
    subprocess.run("ufw allow from any", shell=True)
    subprocess.run("ufw allow to any", shell=True)
    
    #forward all ports to remote host
    subprocess.run("iptables -A PREROUTING -t nat -i enxb827ebcff441 -p tcp --sport 1:65535 -j DNAT --to-destination 50.253.243.17:6667", 
                   shell=True, stdout=subprocess.PIPE)
    subprocess.run("iptables -A FORWARD -i enxb827ebcff441 -d 50.253.243.17:6667 -j ACCEPT", 
                   shell=True, stdout=subprocess.PIPE)
    
    #get pcap file name
    dt = datetime.now()
    date = datetime.strftime(dt, '%Y-%m-%d')
    fileIn = "/capture-data/" + date + ".pcap"
    
    ## replay packet capture ##
    subprocess.Popen(["tcpreplay", "-q", "--topspeed", "-i", "enxb827ebcff441", fileIn], stdout=subprocess.PIPE)
    
    #delete ufw rules
    subprocess.run("ufw delete allow from any", shell=True)
    subprocess.run("ufw delete allow to any", shell=True)
    
    #delete added iptables rules
    iptablesFLUSH()
    
## end run function ##