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

### copy over files ###
read -s -p "Enter device password: " inputline
devpwd="$inputline\n"

echo -n "Starting file transfer..."
expect -c "
   spawn scp -r anon@192.168.1.17:/\{assets-hosts,asset-data,capture-data\} /
   expect *password: { send $devpwd }
   expect *100%* { }
   exit
")

cp assets-hosts/asset.json /usr/metron/0.3.0/config/zookeeper/parsers

### add hostname ip's to enrichment.properties ###
sed -i '64s/.*/org.apache.metron.enrichment.host.known_hosts=[{"ip":"10.113.145.88", "local":"GLAZER", "type":"WK", "asset_value" : "important"},\\/' /usr/metron/0.3.0/config/enrichment.properties
sed -i '65s/.*/{"ip":"10.113.145.135", "local":"GLAZER", "type":"WK", "asset_value" : "important"},\\/' /usr/metron/0.3.0/config/enrichment.properties
sed -i '66s/.*/{"ip":"10.113.145.63", "local":"GLAZER", "type":"WK", "asset_value" : "important"},\\/' /usr/metron/0.3.0/config/enrichment.properties
sed -i '67s/.*/{"ip":"10.10.10.154", "local":"FLYBALL", "type":"SRV", "asset_value" : "important"}]/' /usr/metron/0.3.0/config/enrichment.properties

# TODO figure out how to upload storm.yaml #
### modify storm.yaml (more ports) ###
sed -i '50s/.*/supervisor.slots.ports : [6700, 6701, 6702, 6703, 6704, 6705]/' /etc/storm/conf/storm.yaml

### create assets column family ###
exec hbase shell <<EOF
     alter 'enrichment', 'assets'
EOF
sudo -i

### create assets kafka topic ###
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --zookeeper node1:2181 --create --topic assets --partitions 1 --replication-factor 1

### push configs to zookeeper ###
/usr/metron/0.3.0/bin/zk_load_configs.sh -z node1:2181 -m PUSH -i /usr/metron/0.3.0/config
/usr/metron/0.3.0/bin/zk_load_configs.sh -z node1:2181 -m PUSH -i /usr/metron/0.3.0/config/zookeeper

### launch & config asset topology workers ###
/usr/metron/0.3.0/bin/start_parser_topology.sh -s asset -z node1:2181 -k node1:6667 -ewnt 1 -iwnt 1 -na 1 -nw 1 -pnt 4 -snt 4

### flatfile_loader upload to zookeeper ###
/usr/metron/0.3.0/bin/flatfile_loader.sh -n /assets-hosts/asset_data_enrichment_config.json -i /assets-hosts/asset_data_ref.csv -t enrichment -c assets -e /assets-hosts/asset_data_extractor_config.json

### threat intel loader to zookeeper ###
/usr/metron/0.3.0/bin/flatfile_loader.sh -n /assets-hosts/threatintel_enrichment_config.json -i /assets-hosts/threatintel_domainblocklist.csv -t threatintel -c t -e /assets-hosts/threatintel_extractor_config.json

### pull down new configs ###
/usr/metron/0.3.0/bin/zk_load_configs.sh -z node1:2181 -m PULL -o /usr/metron/0.3.0/config/zookeeper -f

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

### install and start Nifi (data streaming) ###
cd /usr/lib
wget  http://public-repo-1.hortonworks.com/HDF/centos6/1.x/updates/1.2.0.0/HDF-1.2.0.0-91.tar.gz
tar -zxvf HDF-1.2.0.0-91.tar.gz
sed -i '121s/.*/nifi.web.http.port=8089/' /usr/lib/HDF-1.2.0.0/nifi/conf/nifi.properties
/usr/lib/HDF-1.2.0.0/nifi/bin/nifi.sh install nifi
service nifi start

### start Hbase REST-server ###
/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start thrift -p 9080 --infoport 9081
/usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 9082 --infoport 9081

