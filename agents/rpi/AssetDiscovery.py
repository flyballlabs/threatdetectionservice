'''
This script scans devices on the net
and sends aseet informatino to metron
@author: devopsec
'''

import subprocess, sys, io, re
from asyncio.tasks import wait

def replace_deficit():
    if deficit_fields == 4:
        output.write('"","","",""\n') 
    elif deficit_fields == 3:
        output.write('"","",""\n')
    elif deficit_fields == 2:
        output.write('"",""\n')
    elif deficit_fields == 1:
        output.write('""\n')
### end replace_deficit function ###

fileOut = "/asset-data/scanned.txt"

print("starting scan")
scan = subprocess.Popen(['nmap', '-v', '-O', '--osscan-guess', '-T', '4',  '10.113.145.*'], universal_newlines=True, stdout=subprocess.PIPE)
try:
    scan.wait(timeout=14400) #4hr limit
except subprocess.TimeoutExpired:
    print("Exceeded 4hr limit, terminating scan")
    scan.terminate()
try:
    data = scan.communicate(timeout=1800)[0] #30 min limit
except subprocess.TimeoutExpired:
    print("Exceeded 10min limit, killing and retrying communication")
    scan.kill()
    data = scan.communicate()[0]
print("end of scan")

print("start writing data to file")
output = open(fileOut, "w")
output.write(data)
output.close()
print("end writing data to file")

print("starting filter")
# filter for fields #
filter = subprocess.Popen('grep -E "Nmap scan report for|MAC Address:|Device type:|Running:|OS details:" /asset-data/scanned.txt', 
                          shell=True, stdout=subprocess.PIPE, universal_newlines=True)

try:
    filter.wait(timeout=900) #15min limit
except subprocess.TimeoutExpired:
    print("Exceeded 15min limit, terminating filter")
    filter.terminate()
try:
    data = filter.communicate(timeout=600)[0] #10 min limit
except subprocess.TimeoutExpired:
    print("Exceeded 10min limit, killing and retrying communication")
    filter.kill()
    data = filter.communicate()[0]
print("end of filter")

print("start writing data to file")
fileOut = "/asset-data/filtered.txt"
output = open(fileOut, "w")
output.write(data)
output.close()
print("end writing data to file")


print("start of filter2")
# filter out erroneous fields #
filter2 = subprocess.Popen('grep -v "host down" /asset-data/filtered.txt', 
                          shell=True, stdout=subprocess.PIPE, universal_newlines=True)
try:
    filter2.wait(timeout=900) #15min limit
except subprocess.TimeoutExpired:
    print("Exceeded 15min limit, terminating filter")
    filter2.terminate()
try:
    data = filter2.communicate(timeout=600)[0] #10 min limit
except subprocess.TimeoutExpired:
    print("Exceeded 10min limit, killing and retrying communication")
    filter2.kill()
    data = filter2.communicate()[0]
print("end of filter2")


print("start writing data to file")
fileOut = "/asset-data/filtered2.txt"
output = open(fileOut, "w")
output.write(data)
output.close()
print("end writing data to file")

print("start parsing data")
# filter out other strings from lines & format as csv #
output = open('/asset-data/filtered_data.csv', 'w')
input = open("/asset-data/filtered2.txt", "r")
deficit_fields = 0
for line in input:
    global deficit_fields
    if re.search("Nmap", line) != None:
        if deficit_fields != 0:
            replace_deficit()
        str = re.sub(', ', ' ', line)
        str = re.sub('[^0-9.]', '', str)
        output.write(str + ',')
        deficit_fields = 4
    elif re.search("MAC", line) != None:
        str = re.sub('MAC Address: ', '', line)
        str = re.split(' ', str)
        str = str[0]
        output.write(str + ',')
        deficit_fields = 3
    elif re.search("Device", line) != None:
        str = re.sub('Device type: ', '', line)
        str = re.sub('\n', '', str)
        output.write(str + ',')
        deficit_fields = 2
    elif re.search("Running", line) != None:
        str = re.sub('Running: ', '', line)
        str = re.sub(', ', ' ', str)
        str = re.sub('\n', '', str)
        output.write(str + ',')
        deficit_fields = 1
    elif re.search("OS", line) != None:
        str = re.sub('OS details: ', '', line)
        str = re.sub('( or |, or )', '|', str)
        str = re.sub(', ', ' ', str)
        output.write(str)
        deficit_fields = 0
else:
    input.close()
    output.close()
print("end parsing data")

# send data via kafka #
send = subprocess.Popen("tail /asset-data/filtered_data.csv | /kafka/bin/kafka-console-producer.sh --broker-list 50.253.243.17:6667 --topic assets --new-producer", 
                        shell=True, stdout=subprocess.PIPE)
try:
     send.wait(timeout=1800) #30min limit
except subprocess.TimeoutExpired:
    print("Exceeded 30min limit, terminating kafka producer")
    send.terminate()
sys.exit()