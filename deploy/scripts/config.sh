#!/bin/bash
# jq must be installed prior to running #
# to install jq: sudo apt-get install jq #

# runs as su, no pw prompt #
sudo -i

# install / update pre-reqs for ambari #
yum -y install epel-release
yum update -y
yum -y install git wget curl rpm scp tar unzip wget createrepo reposync yum-utils ntp python-pip
pip install --upgrade pip setuptools

### copy over files ###
echo "Copying files to config dirs..."
cp /assets-hosts/asset.json /usr/metron/0.3.0/config/zookeeper/parsers
mv /ojdbc6.jar /usr/hdp/2.5.3.0-37/hadoop/lib/ojdbc6.jar

### add hostname ip's to enrichment.properties ###
sed -i '64s/.*/org.apache.metron.enrichment.host.known_hosts=[{"ip":"10.113.145.88", "local":"GLAZER", "type":"WK", "asset_value" : "important"},\\/' /usr/metron/0.3.0/config/enrichment.properties
sed -i '65s/.*/{"ip":"10.113.145.135", "local":"GLAZER", "type":"WK", "asset_value" : "important"},\\/' /usr/metron/0.3.0/config/enrichment.properties
sed -i '66s/.*/{"ip":"10.113.145.63", "local":"GLAZER", "type":"WK", "asset_value" : "important"},\\/' /usr/metron/0.3.0/config/enrichment.properties
sed -i '67s/.*/{"ip":"10.10.10.154", "local":"FLYBALL", "type":"SRV", "asset_value" : "important"}]/' /usr/metron/0.3.0/config/enrichment.properties

# Disable packagekit if installed #
cmnd=$(yum list | grep "PackageKit")
eval "${cmnd}"
if [ $? -eq 0 ]; then
	sed -i 's/enabled=1/enabled=0/g' /etc/yum/pluginconf.d/refresh-packagekit.conf
fi

# Increase limits for ElasticSearch and Storm #
echo -e "elasticsearch - memlock unlimited\nstorm - nproc 257597" >> /etc/security/limits.conf

# Disable IPv6, leaving it enabled may force service to bind to IPv6 addresses only #
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
echo -e "\n# Disable IPv6\nnet.ipv6.conf.all.disable_ipv6 = 1\nnet.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf

# Disable Transparent Hugepage #
sed '/Line16/ s/$/ transparent_hugepage=never/' /etc/grub.conf
sed '/Line20/ s/$/ transparent_hugepage=never/' /etc/grub.conf

# TODO figure out how to upload storm.yaml #
### modify storm.yaml (more ports) ###
sed -i '50s/.*/supervisor.slots.ports : [6700, 6701, 6702, 6703, 6704, 6705]/' /etc/storm/conf/storm.yaml

### create assets column family ###
exec hbase shell <<EOF
     alter 'enrichment', 'assets'
EOF

### create assets kafka topic ###
/usr/hdp/current/kafka-broker/bin/kafka-topics.sh --zookeeper node1:2181 --create --topic assets --partitions 1 --replication-factor 1

### push configs to zookeeper ###
/usr/metron/$METRON_VERSION/bin/zk_load_configs.sh -z node1:2181 -m PUSH -i /usr/metron/$METRON_VERSION/config
/usr/metron/$METRON_VERSION/bin/zk_load_configs.sh -z node1:2181 -m PUSH -i /usr/metron/$METRON_VERSION/config/zookeeper

### launch & config asset topology workers ###
/usr/metron/$METRON_VERSION/bin/start_parser_topology.sh -s asset -z node1:2181 -k node1:6667 -ewnt 1 -iwnt 1 -na 1 -nw 1 -pnt 4 -snt 4

### flatfile_loader upload to zookeeper ###
/usr/metron/$METRON_VERSION/bin/flatfile_loader.sh -n /assets-hosts/asset_data_enrichment_config.json -i /assets-hosts/asset_data_ref.csv -t enrichment -c assets -e /assets-hosts/asset_data_extractor_config.json

### threat intel loader to zookeeper ###
/usr/metron/$METRON_VERSION/bin/flatfile_loader.sh -n /assets-hosts/threatintel_enrichment_config.json -i /assets-hosts/threatintel_domainblocklist.csv -t threatintel -c t -e /assets-hosts/threatintel_extractor_config.json

### pull down new configs ###
/usr/metron/$METRON_VERSION/bin/zk_load_configs.sh -z node1:2181 -m PULL -o /usr/metron/$METRON_VERSION/config/zookeeper -f

timestamp=$(($(date +%s%N)/1000000))
CLUSTER_CONFIGS=$(curl -u admin:admin -H "X-Requested-By: ambari" -X GET  http://$AMBARI_UI/api/v1/clusters/$CLUSTER_NAME?fields=Clusters/desired_configs | jq .Clusters.desired_configs)

curl -u admin:admin -H "X-Requested-By: ambari" -X GET "http://$AMBARI_UI/api/v1/clusters/$CLUSTER_NAME/configurations?type=kafka-broker&tag=version1478946130445"

# TODO: add external hostname configs using cmd below if flag is present #
#curl -u admin:admin -H "X-Requested-By: ambari" -X PUT -d '[{"Clusters":{
#  "desired_config":[{
#    "type":"zoo.cfg",
#    "tag":"version'"$timestamp"'",
#    "properties":{
#      "autopurge.purgeInterval":"24",
#      "autopurge.snapRetainCount":"30",
#      "dataDir":"/hadoop/zookeeper",
#      "tickTime":"2000",
#      "initLimit":"11",
#      "syncLimit":"5",
#      "clientPort":"2181"},
#    "service_config_version_note":"New config version"}]}}]'
#"http://AMBARI_SERVER_HOST:8080/api/v1/clusters/CLUSTER_NAME"

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

