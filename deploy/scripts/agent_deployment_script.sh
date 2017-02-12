#!/bin/bash
# Author: devopsec
# Summary: Deployment script for agent configuration.

cd /

# get current ip / make sure connected to internet #
IP=$(ip route get 8.8.8.8 | awk 'NR==1 {print $NF}')
if [[ -n $(echo "$IP" | grep -i "unreachable") ]]; then
    echo "Not connected to internet. Exiting.."
    exit 1
fi
echo "Current IP address of agent: $IP"

# ensure git is installed #
TEMP=$(dpkg -l "git" 2>&1 | grep -i "no packages found")
if [[ -n "$TEMP" ]]; then
	echo "installing git.."
	DEBIAN_FRONTEND=noninteractive apt-get install git
	git --version
fi

# set hostname #
function setHostName(company, site, agent_id) {
    hostname -b "$1_$2_$3";
}

git clone --recursive https://github.com/flyballlabs/threatdetectionservice.git
cd /threatdetectionservice

#TODO: move files where they need to go
#TODO: set hostname
#TODO: set cron jobs to run
#TODO: set environment variables
#TODO: install any other dependencies such as kafka, pycapy, tcpdump
