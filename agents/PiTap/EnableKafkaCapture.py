'''
This script enables Kafka listening
for rPi captured data
@author: devopsec
'''

import subprocess

def kafkaCapture():
    
    #allow traffic on port 6667
    subprocess.call("ufw allow 6667", shell=True)
    
    #start kafka producer
    subprocess.call("pycapa --producer --kafka node1:6667 --topic pcap -i eno1", shell=True)
    
return None