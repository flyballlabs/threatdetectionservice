'''
This script disables packet capture
on rPi network tap
Make sure to re-enable ports after
@author: devopsec
'''

def disableCapture():
    
    import subprocess
    from rpi import EnableCapture
    
    #send sigint
    subprocess.run("signal.SIGINT", shell=True)
    try:
        os.kill(pid, EnableCapture.pCap.pid)
    except:
        pass
        
    #flush iptables
    
    # IPv6
    ## set default policies to let everything in
    subprocess.run("ip6tables --policy INPUT   ACCEPT", shell=True)
    subprocess.run("ip6tables --policy OUTPUT  ACCEPT", shell=True)
    subprocess.run("ip6tables --policy FORWARD ACCEPT", shell=True)
    ## start fresh
    subprocess.run("ip6tables -Z; # zero counters", shell=True)
    subprocess.run("ip6tables -F; # flush (delete) rules", shell=True)
    subprocess.run("ip6tables -X; # delete all extra chains", shell=True)
    # IPv4
    ## set default policies to let everything in
    subprocess.run("iptables --policy INPUT   ACCEPT", shell=True)
    subprocess.run("iptables --policy OUTPUT  ACCEPT", shell=True)
    subprocess.run("iptables --policy FORWARD ACCEPT", shell=True)
    ## start fresh
    subprocess.run("iptables -Z; # zero counters", shell=True)
    subprocess.run("iptables -F; # flush (delete) rules", shell=True)
    subprocess.run("iptables -X; # delete all extra chains", shell=True)
    
    #reset ufw settings
    subprocess.run("ufw default deny incoming", shell=True)
    subprocess.run("ufw default allow outgoing", shell=True)
    
    return None