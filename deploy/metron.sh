#!/bin/bash

### function definitions ###
start_cluster() {
	echo "starting metron cluster"
	cd /incubator-metron/metron-deployment/vagrant/quick-dev-platform
	vagrant up
	sleep 15 # wait for cluster to start up
}

start_services() {
	echo "starting metron services" 
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start HDFS via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/HDFS
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start YARN via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/YARN
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start MAPREDUCE2 via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/MAPREDUCE2
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start Hbase via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/Hbase
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start ZOOKEEPER via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/ZOOKEEPER
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start Storm via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/Storm
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start Kafka via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/Kafka
}

stop_cluster() {
	echo "stopping metron cluster"
	cd /incubator-metron/metron-deployment/vagrant/quick-dev-platform
	vagrant halt
	sleep 15 # wait for cluster to halt
}

stop_services() {
	echo "stopping metron services" 
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop HDFS via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/HDFS
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop YARN via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/YARN
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop MAPREDUCE2 via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/MAPREDUCE2
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop Hbase via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/Hbase
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop ZOOKEEPER via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/ZOOKEEPER
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop Storm via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/Storm
	curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop Kafka via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://${AMBARI_UI}/api/v1/clusters/$CLUSTER_NAME/services/Kafka
}

### arg parsing ###
cmd=""  # Default none

HELP() {
	echo "Usage: "
	echo "metron -h                 Display this help message."
	echo "metron --start <cmd>      Start <cmd> from list of start cmds."
	echo "metron --stop  <cmd>      Stop <cmd> from list of stop cmds."
	echo "Available <cmd> options:  cluster, service"
}

#Check the number of arguments. If none are passed, print help and exit
options=$(getopt -o h: -l start:,stop: -n metron -- "$@")
if [ $? -eq 0 ]; then
	echo $0
	echo $#
	echo $?
	echo $*
	HELP
	exit 1
fi

### parse options ###
eval set -- "$options"
while true; do
    case "$1" in
		-h ) 
			HELP # Show help option menu
			;;
		--start ) # Parse options to start sub command
			cmd=$1 # Remove 'start' from the argument list
			shift;
			if [[ cmd == "cluster" ]]; then
				start_cluster
			elif [[ cmd == "service" ]]; then
				start_services
			fi
			;;
		--stop ) # Parse options to start sub command
			cmd=$1 # Remove 'stop' from the argument list
			shift;
			if [[ cmd == "cluster" ]]; then
				start_cluster
			elif [[ cmd == "service" ]]; then
				start_services
			fi
			;;
		-- ) 
			shift
			break
			;;
	esac
done
exit 0
