#!/bin/bash
# jq must be installed prior to running #
# to install jq: sudo apt-get install jq #

### Metron (host) external forwarding settings ###
-A FORWARD -i enp0s31f6 -o vboxnet0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i vboxnet0 -o enp0s31f6 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 8080 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT
-A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 5000 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j AC:CEPT
-A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 8744 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT
-A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 2812 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT
-A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 6667 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT


timestamp=$(($(date +%s%N)/1000000))
CLUSTER_CONFIGS=$(curl -u admin:admin -H "X-Requested-By: ambari" -X GET  http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME?fields=Clusters/desired_configs | jq .Clusters.desired_configs)

curl -u admin:admin -H "X-Requested-By: ambari" -X GET "http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/configurations?type=kafka-broker&tag=version1478946130445"

curl -u admin:admin -H "X-Requested-By: ambari" -X PUT -d '[{"Clusters":{
  "desired_config":[{
    "type":"zoo.cfg",
    "tag":"version'"$timestamp"'",
    "properties":{
      "autopurge.purgeInterval":"24",
      "autopurge.snapRetainCount":"30",
      "dataDir":"/hadoop/zookeeper",
      "tickTime":"2000",
      "initLimit":"11",
      "syncLimit":"5",
      "clientPort":"2181"},
    "service_config_version_note":"New config version"}]}}]'
"http://AMBARI_SERVER_HOST:8080/api/v1/clusters/CLUSTER_NAME"

#Key: advertised.host.name   Value: <metron-hostname> 
#Key: advertised.listeners   Value: PLAINTEXT://<external-ip>:6667
# add external ip and metron-hostname to /etc/hosts (on vm) #
## Key: host.name Value: node1:6667 ## what the broker binds to ##
## Key: zookeeper.connect Value: <internal zookeeper ip> ##
## Key: advertised.host.name Value: <public ip> ##
## Key: metadata.broker.list Value: node1:6667 ##
#######################################################

### kill example pcap replay ###
# disable monit from monitoring pcap replay #
service pcap-replay stop
killall tcpreplay
# flush kibana index #
curl -XDELETE node1:9200/bro*


### start Nifi (data streaming server) ###
service nifi start

### start Hbase REST-server ###
/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start thrift -p 9080 --infoport 9081
/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 9082 --infoport 9081

