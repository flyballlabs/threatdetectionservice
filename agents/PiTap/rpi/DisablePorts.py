'''
This script disables ports
on an rPi network tap
@author: devopsec
'''

import subprocess
    
#disable ssh input / output
subprocess.run("ufw deny 22", shell=True)
subprocess.run("iptables -D INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -D OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#disable http input / output
subprocess.run("ufw denu 80", shell=True)
subprocess.run("iptables -D INPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -D OUTPUT -p tcp --sport 80 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D INPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D OUTPUT -p tcp --sport 80 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#disable forward ssh on 2222
subprocess.run("iptables -D PREROUTING -t nat -p 22 --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("iptables -D FORWARD -p 22 -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
subprocess.run("ip6tables -D PREROUTING -t nat -p 22 --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("ip6tables -D FORWARD -p 22 -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
#disable forward http on 1008
subprocess.run("iptables -D PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("iptables -D FORWARD -p tcp -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
subprocess.run("ip6tables -D PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("ip6tables -D FORWARD -p tcp -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
#stop ssh service
subprocess.run("service ssh stop", shell=True)


