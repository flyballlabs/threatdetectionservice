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

# Function responsible for installing TMP

install_tmp() {

	echo "About to install Threat Management Platform"
	
	vagrant ssh -c 'sudo rm -rf /usr/threatmanagementplatform'
	vagrant ssh -c 'sudo mkdir /usr/threatmanagementplatform'
	if [ $? -eq 1 ]; then
	
		echo "The directory for configuration files could not be created"
		exit
	fi	

	scp -r -P 2222 -i $SSH_PRIVATE_KEY ~/threatdetectionservice/metron vagrant@127.0.0.1:.
	if [ $? -eq 0 ]; then

		echo "The Metron files have been copied sucessfully"
	
	fi

	vagrant ssh -c 'sudo mv ~/metron /usr/threatmanagementplatform'
	if [ $? -eq 1 ]; then
	
		echo "The directory for configuration files could not be created"
		exit
	fi	
	
}

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

scp -P 2222 -i $SSH_PRIVATE_KEY ~/mack.txt vagrant@127.0.0.1:.
if [ $? -eq 0 ]; then

	echo "Test file was sent over"
fi

METRON_VERSION=`vagrant ssh -c 'ls /usr/metron'`
METRON_VERSION=`echo $METRON_VERSION | cut -d " " -f 11`
#echo $METRON_VERSION

if [ -z "${METRON_VERSION+x}" ]; then

	echo "Metron doesn't seem to be installed.  Metron has to be installed before Installing the Threat Management Platform"
else
	echo "Metron Version Detected: $METRON_VERSION"
	install_tmp
fi


#Find out which version of Metron is installed

#Create a directory for TMP Specific stuff

#Copy over TMP files

#Load configs into Storm 

#Config Kafka as needed

#Setup SFTP landing zones for PCAP files
