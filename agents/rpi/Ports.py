'''
This script allows config of ports on rPi network tap
@author: devopsec
'''

import socket, subprocess

'''
@summary: 
This class holds functions for configuring ports
'''
class func:
    def getIPAddress():
        output = subprocess.check_output(['hostname', '-I'])
        return output
	

    def check():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipAddress = func.getIPAddress() 

        ## check HTTP ports ##
        check = sock.connect_ex((ipAddress,80))
        if check == 0:
            port80 = True
        else:
            port80 = False
            
        check = sock.connect_ex((ipAddress,1008))
        if check == 0:
            port1008 = True
        else:
            port1008 = False
        
        ## check SSH ports ##
        check = sock.connect_ex((ipAddress,22))
        if check == 0:
            port22 = True
        else:
            port22 = False
        
        check = sock.connect_ex((ipAddress,2222))
        if check == 0:
            port2222 = True
        else:
            port2222 = False
        
        sock.close()
        return (port80, port1008, port22, port2222)
    ## end check function ##
    
    def enable():
        #ensure ufw is enabled
        subprocess.run("ufw enable", shell=True)
        
        #enable ssh input / output
        subprocess.run("ufw allow 22", shell=True)
        subprocess.run("iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        
        #enable http input / output
        subprocess.run("ufw allow 80", shell=True)
        subprocess.run("iptables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("iptables -A OUTPUT -p tcp --sport 80 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -A INPUT -p tcp --dport 80 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -A OUTPUT -p tcp --sport 80 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        
        #start ssh service
        subprocess.run("service ssh start", shell=True)
    ## end enable function ##
    
    def disable():
        ## disable ssh input / output ##
        subprocess.run("ufw delete allow 22", shell=True)
        subprocess.run("iptables -D INPUT -p tcp --dport 2222 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("iptables -D OUTPUT -p tcp --sport 2222 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -D INPUT -p tcp --dport 2222 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -D OUTPUT -p tcp --sport 2222 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        
        #disable http input / output
        subprocess.run("ufw delete allow 80", shell=True)
        subprocess.run("iptables -D INPUT -p tcp --dport 1008 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("iptables -D OUTPUT -p tcp --sport 1008 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -D INPUT -p tcp --dport 1008 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT", shell=True)
        subprocess.run("ip6tables -D OUTPUT -p tcp --sport 1008 -m conntrack --ctstate ESTABLISHED -j ACCEPT", shell=True)
        
        #stop ssh service
        subprocess.run("service ssh stop", shell=True)
    ## end disable function ##

