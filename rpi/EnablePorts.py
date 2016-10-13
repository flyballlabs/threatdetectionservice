'''
This script enables ports
on an rPi network tap
@author: devopsec
'''

import subprocess

#ensure ufw is enabled
subprocess.run("ufw enable", shell=True)

#enable ssh input / output
subprocess.run("ufw allow 22", shell=True)
subprocess.run("ufw allow 2222", shell=True)
subprocess.run("iptables -A INPUT -p tcp --dport 2222 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -A OUTPUT -p tcp --sport 2222 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A INPUT -p tcp --dport 2222 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A OUTPUT -p tcp --sport 2222 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#enable http input / output
subprocess.run("ufw allow 80", shell=True)
subprocess.run("ufw allow 1008", shell=True)
subprocess.run("iptables -A INPUT -p tcp --dport 1008 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("iptables -A OUTPUT -p tcp --sport 1008 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A INPUT -p tcp --dport 1008 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
subprocess.run("ip6tables -A OUTPUT -p tcp --sport 1008 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)

#enable forward ssh on 2222
subprocess.run("iptables -A PREROUTING -t nat -p tcp --dport 22 -j DNAT --to 10.113.145.149:2222", shell=True)
subprocess.run("iptables -A FORWARD -p tcp -d 10.113.145.149 --dport 2222 -j ACCEPT", shell=True)
subprocess.run("ip6tables -A PREROUTING -t nat -p tcp --dport 22 -j DNAT --to 10.113.145.149:2222", shell=True)
subprocess.run("ip6tables -A FORWARD -p tcp -d 10.113.145.149 --dport 2222 -j ACCEPT", shell=True)

#enable forward http on 1008
subprocess.run("iptables -A PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.113.145.149:1008", shell=True)
subprocess.run("iptables -A FORWARD -p tcp -d 10.113.145.149 --dport 1008 -j ACCEPT", shell=True)
subprocess.run("ip6tables -A PREROUTING -t nat -p tcp --dport 80 -j DNAT --to 10.113.145.149", shell=True)
subprocess.run("ip6tables -A FORWARD -p tcp -d 10.113.145.149 --dport 1008 -j ACCEPT", shell=True)

#start ssh service
subprocess.run("service ssh start", shell=True)
