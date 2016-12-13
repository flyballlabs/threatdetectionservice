from starbase import Connection
import pyshark

metronHBaseRestURL="http://10.10.10.154"
metronHbaseRestPort = 9082
metronHBaseTable = "enrichment"
metronHBaseCF="assets"

#get this data from pcap#
company_name = "Flyball-Labs"
site = "glazer"  

pcap = pyshark.FileCapture('/capture-data/2016-10-24.pcap', display_filter='udp.port == 5353', keep_packets=False) #only_summaries=True
data = []
def run(pkt):
    i = 1
    try:
        ip = pkt.mdns.dns_a
        target = pkt.mdns.dns_srv_target.split(sep='.')
        host = target[0]
        
        if host != None and ip != None:
            rowkey = company_name + "_" + site + "_" + ip
            t.insert(rowkey,{metronHBaseCF: {'hostname': host}})
        
        ## debug ##

        print(data[i])
    except Exception as e:
        pass
    i += 1

## setup table
c = Connection(host=metronHBaseRestURL, port=metronHbaseRestPort)
t = c.table(metronHBaseTable)   
if t.exists() == True:
    pcap.apply_on_packets(run) ## start parsing

#while True:
#    print(pcap[0])   

###Filters and Other Options###s
#pcap.display_filter='smb || nbns || dcerpc || nbss || dns'
'''def get_capture_count():
    p = pyshark.FileCapture('/capture-data/2016-10-24.pcap', keep_packets=False)
 
    count = []
    def counter(*args):
        count.append(args[0])
 
    p.apply_on_packets(counter, timeout=100000)
 
    return len(count)
print(get_capture_count())'''

'''* **param keep_packets**: Whether to keep packets after reading them via next().
Used to conserve memory when reading large caps.
* **param input_file**: Either a path or a file-like object containing either a
packet capture file (PCAP, PCAP-NG..) or a TShark xml.
* **param display_filter**: A display (wireshark) filter to apply on the cap
before reading it.
* **param only_summaries**: Only produce packet summaries, much faster but includes
very little information
* **param decryption_key**: Key used to encrypt and decrypt captured traffic.
* **param encryption_type**: Standard of encryption used in captured traffic (must
be either 'WEP', 'WPA-PWD', or 'WPA-PWK'. Defaults to WPA-PWK.
* **param tshark_path**: Path of the tshark binary'''

###Decrypting packet captures
#Pyshark supports automatic decryption of traces using the WEP, WPA-PWD, and WPA-PSK standards (WPA-PWD is the default).

#cap1 = pyshark.FileCapture('/tmp/capture1.cap', decryption_key='password')
#cap2 = pyshark.LiveCapture(interface='wi0', decryption_key='password', encryption_type='wpa-psk')
