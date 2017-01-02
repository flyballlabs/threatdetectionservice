#!/bin/bash

# Author: devopsec and mackhendricks
# Summary: This deployment script is focused on configuring a metron environment 
# with the configs and programs needed by the Threat Mananagement Platform API to work
# properly
# Note: This script must be run as root user to work properly.
# Note: Platform must be a unix-based x64 architecture os.

# Version 1.0
# - Focused on working with Metron Vagrant Install

### Sudo Code ###

#Check if the Vagrant VM of Metron is installed and up

# This can be the Vagrant file for the Quick Dev Install, Code Lab, Full Install, etc
# If this is not set, we will prompt for the location

METRON_VAGRANT_DIR=/incubator-metron/metron-deployment/vagrant/quick-dev-platform

if [ -z "${METRON_VAGRANT_DIR+x}" ]; then

	echo "Please provide the directory that contains your Metron Vagrant File"
	read METRON_VAGRANT_DIR
fi

echo "Vagrant Directory Used: $METRON_VAGRANT_DIR"

# Use the built-in environment variable to specify the Vagrantfile to use
# when 

VAGRANT_VAGRANTFILE=$METRON_VAGRANT_DIR/Vagrantfile

echo "Vagrant File Used: $VAGRANT_VAGRANTFILE"
cd $METRON_VAGRANT_DIR
SSH_PRIVATE_KEY=`vagrant ssh-config | grep IdentityFile | awk '{print $2}'|sed 's/\"//g'`
echo "Vagrant SSH_PRIVATE_KEY:$SSH_PRIVATE_KEY"

scp -P 2222 -i $SSH_PRIVATE_KEY ~/test.txt vagrant@127.0.0.1:.
if [ $? -eq 0 ]; then

	echo "Test file was sent over"
fi


#Find out which version of Metron is installed

#Create a directory for TMP Specific stuff

#Copy over TMP files

#Load configs into Storm 

#Config Kafka as needed

#Setup SFTP landing zones for PCAP files
