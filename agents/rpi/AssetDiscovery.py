'''
This script scans devices on the net
and sends aseet informatino to metron
@author: devopsec
'''

import subprocess, sys, io, re, csv
from asyncio.tasks import wait

fileOut = "/asset-data/scanned.txt"

print("starting scan")
scan = subprocess.Popen(['nmap', '-v', '-O', '-T', '5', '--osscan-guess', '10.113.145.*'], universal_newlines=True, stdout=subprocess.PIPE)
try:
    scan.wait(timeout=3600) #1hr limit
except subprocess.TimeoutExpired:
    print("Exceeded 1hr limit, terminating scan")
    scan.terminate()
try:
    data = scan.communicate(timeout=600)[0] #10 min limit
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


print("start of filter")
# filter out erroneous fields #
filter = subprocess.Popen('grep -v "host down" /asset-data/filtered.txt', 
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
fileOut = "/asset-data/filtered2.txt"
output = open(fileOut, "w")
output.write(data)
output.close()
print("end writing data to file")


print("start parsing data")
# filter out other strings from lines & format as csv #
output = open(fileOut, "r+")
data = output.read()

for line in data:
    if re.match('Nmap', line) != None:
        re.sub('[^0-9.]', '', line)
    if re.match('MAC', line) != None:
        re.sub('MAC Address: ', '', line)
        re.split(' ', line)
        str = line[0]
        line.replace(line, str)
    else:
        line.replace(line, line + '""' + "\n")
    if re.match('Device', line) != None:
        re.sub('Device type: ', '', line)
    else:
        line.replace(line, line + '""' + "\n")
    if re.match('Running', line) != None:
        re.sub('Running: ', '', line)
        re.sub(', ', '|', line)
    else:
        line.replace(line, line + '""' + "\n")
    if re.match('OS', line) != None:
        re.sub('OS details: ', '', line)
        re.sub('(, |, or |)', '/', line)
        re.sub(' or ', '||', line)
    else:
        line.replace(line, line + '""' + "\n")
        
# debug #
file_loc = "/asset-data/debug.txt"
file = open(file_loc, 'w')
file.write(line)
file.close()
# end debug #

# parse text file to csv #
csv_out = "/asset-data/filtered_data.csv"
#in_txt = csv.reader(output, delimiter = '\n')
with open(csv_out, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter='\n')
        writer.writerows(output)
output.close()
print("end parsing data")

# send data via kafka #
send = subprocess.Popen("tail /asset-data/filtered_data.csv | /kafka/bin/kafka-console-producer.sh --broker-list 50.253.243.17:6667 --topic assets", 
                        shell=True, stdout=subprocess.PIPE)
try:
    send.wait(timeout=900) #15min limit
except subprocess.TimeoutExpired:
    print("Exceeded 10min limit, terminating filter")
    send.terminate()