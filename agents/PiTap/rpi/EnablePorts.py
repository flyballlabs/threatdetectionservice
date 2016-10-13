'''
This script enables ports
on an rPi network tap
@author: devopsec
'''

import subprocess

#disable ssh input / output
subprocess.run("ufw allow 22", shell=True)
subprocess.run("iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#disable http input / output
subprocess.run("ufw allow 80", shell=True)
subprocess.run("iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -A OUTPUT -p tcp --sport 80 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A OUTPUT -p tcp --sport 80 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#disable forward ssh on 2222
subprocess.run("iptables -A PREROUTING -t nat -p 22 --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("iptables -A FORWARD -p 22 -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
subprocess.run("ip6tables -A PREROUTING -t nat -p 22 --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("ip6tables -A FORWARD -p 22 -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
#disable forward http on 1008
subprocess.run("iptables -A PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("iptables -A FORWARD -p tcp -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
subprocess.run("ip6tables -A PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.10.10.101:1008", shell=True)
subprocess.run("ip6tables -A FORWARD -p tcp -d 10.10.10.101 --dport 1008 -j ACCEPT", shell=True)
#stop ssh service
subprocess.run("service ssh start", shell=True)
