'''
This script replays pcap capture over
the net to host server
Make sure to re-enable ports after
@author: devopsec
'''


    
#get datetime for timestamp
dt = datetime.now()
date = datetime.strftime(dt, '%Y-%m-%d_%H%M')
fileOut = "/media/anon/5227-FD18/capture-data/" + date + ".pcap"

#delete iptables rules
subprocess.run("iptables -F", shell=True)
subprocess.run("ip6tables -F", shell=True)
#forward all ports to remote host
subprocess.run("iptables -A FORWARD portrange 0-65535 -d 50.253.243.17 --dport 6667 -j ACCEPT", shell=True)
#replay packet captures
subprocess.Popen(["tcpreplay", "-q", "--topspeed", "--intf1=eno1", fileOut], shell=True)
