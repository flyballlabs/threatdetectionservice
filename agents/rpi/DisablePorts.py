'''
This script disables ports on rpi network tap prior to replaying data
@author: devopsec
'''

import subprocess
    
#disable ssh input / output
subprocess.run("ufw delete allow 22", shell=True)
subprocess.run("ufw delete allow 2222", shell=True)
subprocess.run("iptables -D INPUT -p tcp --dport 2222 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -D OUTPUT -p tcp --sport 2222 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D INPUT -p tcp --dport 2222 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D OUTPUT -p tcp --sport 2222 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#disable http input / output
subprocess.run("ufw delete allow 80", shell=True)
subprocess.run("ufw delete allow 1008", shell=True)
subprocess.run("iptables -D INPUT -p tcp --dport 1008 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -D OUTPUT -p tcp --sport 1008 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D INPUT -p tcp --dport 1008 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -D OUTPUT -p tcp --sport 1008 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#disable forward ssh on 2222
subprocess.run("iptables -D PREROUTING -t nat -p tcp --dport 22 -j DNAT --to 10.113.145.149:2222", shell=True)
subprocess.run("iptables -D FORWARD -p tcp -d 10.113.145.149 --dport 2222 -j ACCEPT", shell=True)
subprocess.run("ip6tables -D PREROUTING -t nat -p tcp --dport 22 -j DNAT --to 10.113.145.149:2222", shell=True)
subprocess.run("ip6tables -D FORWARD -p tcp -d 10.113.145.149 --dport 2222 -j ACCEPT", shell=True)

#disable forward http on 1008
subprocess.run("iptables -D PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.113.145.149:1008", shell=True)
subprocess.run("iptables -D FORWARD -p tcp -d 10.113.145.149 --dport 1008 -j ACCEPT", shell=True)
subprocess.run("ip6tables -D PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.113.145.149", shell=True)
subprocess.run("ip6tables -D FORWARD -p tcp -d 10.113.145.149 --dport 1008 -j ACCEPT", shell=True)

#stop ssh service
subprocess.run("service ssh stop", shell=True)


