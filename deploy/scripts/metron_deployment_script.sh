#!/bin/bash
# Author: devopsec and mackhendricks
# Summary: Deployment script for metron to config vars and files.
# Note: This script must be run as root user to work properly.
# Note: Platform must be a unix-based x64 architecture os.

cd /

# get host users pw for later usage #
read -s -p "Enter host user's pw: " HOST_PW
sleep 1

# function to install Oracle JDK & JRE and set paths for vars
function install_java {	
	echo "installing oracle java.."	
	DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:webupd8team/java
	DEBIAN_FRONTEND=noninteractive apt-get update
	DEBIAN_FRONTEND=noninteractive apt-get install oracle-java8-installer
	DEBIAN_FRONTEND=noninteractive apt-get install oracle-java8-set-default
	echo 'JAVA_HOME="/usr/lib/jvm/java-8-oracle"' >> /etc/hosts;
	echo 'JRE_HOME="/usr/lib/jvm/java-8-oracle/jre' >> /etc/hosts;
	echo 'PATH=/apache-maven-3.3.9/bin:$JAVA_HOME/bin:$JRE_HOME/bin:$PATH' >> /etc/hosts;
	echo 'export JAVA_HOME' >> /etc/hosts;
	echo 'export JRE_HOME' >> /etc/hosts;
	echo 'export PATH' >> /etc/hosts;
	source /etc/profile
}

# function to forward Metron (host) ports external #
function forward_ports {
	iptables -A FORWARD -i enp0s31f6 -o vboxnet0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
	iptables -A FORWARD -i vboxnet0 -o enp0s31f6 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
	iptables -A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 8080 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT
	iptables -A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 5000 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j AC:CEPT
	iptables -A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 8744 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT
	iptables -A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 2812 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT
	iptables -A FORWARD -i enp0s31f6 -o vboxnet0 -p tcp -m tcp --dport 6667 --tcp-flags FIN,SYN,RST,ACK SYN -m conntrack --ctstate NEW -j ACCEPT
}

# check if java is installed
if type -p java; then
    echo "found java executable in PATH"
    JAVA=java
elif [[ -n "$JAVA_HOME" ]] && [[ -x "$JAVA_HOME/bin/java" ]];  then
    echo "found java executable in JAVA_HOME"
    JAVA="$JAVA_HOME/bin/java"
else
    echo "java is not installed"
fi

if [[ "$JAVA" ]]; then
	# Uninstall all versions of openJDK
	TEMP=$("$JAVA" -version 2>&1 | grep -i "openjdk")
	if [-n $TEMP]; then
		echo "uninstalling openjdk.."
		DEBIAN_FRONTEND=noninteractive apt-get purge openjdk-\*
		install_java
	else
		echo "openjdk is not installed"
	fi

    JAVA_VER=$("$JAVA" -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo "java version "${JAVA_VER}" "
else
	install_java
	JAVA_VER=$("$JAVA" -version 2>&1 | awk -F '"' '/version/ {print $2}')
    echo "java version "${JAVA_VER}" "
fi

## install dependencies if not already ##
if uname -a | grep -i "linux"; then
	TEMP=$(dpkg -l "ansible" 2>&1 | grep -i "no packages found")
	TEMP2=$(pip list 2>&1 | grep -i "ansible")
	if [[ -n "$TEMP" ]] && [[ -z "$TEMP2" ]]; then
		echo "installing ansible.."
		DEBIAN_FRONTEND=noninteractive apt-get install software-properties-common
		DEBIAN_FRONTEND=noninteractive apt-add-repository ppa:ansible/ansible
		DEBIAN_FRONTEND=noninteractive apt-get update
		DEBIAN_FRONTEND=noninteractive apt-get install ansible
	fi
	ansible --version

	TEMP=$(python --version 2>&1 | grep "2.7")
	if [[ -n "$TEMP" ]]; then
		echo "Python version: "${TEMP}""
	else
		echo "installing python.."
		DEBIAN_FRONTEND=noninteractive apt-add-repository ppa:fkrull/deadsnakes-python2.7
		DEBIAN_FRONTEND=noninteractive apt-get update
		DEBIAN_FRONTEND=noninteractive apt-get install python2.7 python2.7-dev python-pip python-dev build-essential
		DEBIAN_FRONTEND=noninteractive pip install --upgrade pip
	fi

	TEMP=$(dpkg -l "ansible" 2>&1 | grep -i "no packages found")
	if [[ -n "$TEMP" ]]; then
		echo "installing maven.."
		cd /
		wget -qO "http://www-us.apache.org/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz" | tar xzvf apache-maven-3.3.9-bin.tar.gz
		mvn --version
	fi	
	
	TEMP=$(dpkg -l "vagrant" 2>&1 | grep -i "no packages found")
	if [[ -n "$TEMP" ]]; then
		echo "installing vagrant.."
		wget -O ~/Downloads/vagrant_1.9.1.deb "https://releases.hashicorp.com/vagrant/1.9.1/vagrant_1.9.1_x86_64.deb"
		DEBIAN_FRONTEND=noninteractive dpkg -i ~/Downloads/vagrant_1.9.1.deb
		DEBIAN_FRONTEND=noninteractive apt-get install -f ~/Downloads/vagrant_1.9.1.deb
		vagrant --version
	fi

	TEMP=$(dpkg -l "virtualbox" 2>&1 | grep -i "no packages found")
	if [[ -n "$TEMP" ]]; then
		echo "installing virtualbox.."
		DEBIAN_FRONTEND=noninteractive apt-get install dkms
		wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | apt-key add -
		wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | apt-key add -
		echo "deb http://download.virtualbox.org/virtualbox/debian Yakkety contrib" >> /etc/apt/sources.list
		DEBIAN_FRONTEND=noninteractive apt-get update
		DEBIAN_FRONTEND=noninteractive apt-get install virtualbox-5.1
		echo "vbox version: " $(vboxmanage --version)
	fi
elif uname -a | grep -i "mac"; then
	if ! whichapp 'homebrew' &>/dev/null; then
		echo "installing homebrew.."
		/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	if ! whichapp 'git' &>/dev/null; then
		echo "installing git.."
		brew install git
		git --version
	if ! whichapp 'virtualbox' &>/dev/null; then
		echo "installing virtualbox.."
		brew cask install virtualbox
		echo "vbox version: " $(vboxmanage --version)
	if ! whichapp 'vagrant' &>/dev/null then;
		echo "installing vagrant.."
		brew cask install vagrant
		brew cask install vagrant-manager
		vagrant --version
	if ! whichapp 'maven' &>/dev/null; then
		echo "installing maven.."
		brew install maven
	if ! whichapp 'ansible' &>/dev/null; then
		echo "installing ansible.."
		brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/ee1273bf919a5e4e50838513a9e55ea423e1d7ce/Formula/ansible.rb
		brew switch ansible 2.0.0.2
	fi
fi

# set configs in debconf and install iptables-persistent #
echo "iptables-persistent iptables-persistent/autosave_v4 boolean true" | debconf-set-selections
echo "iptables-persistent iptables-persistent/autosave_v6 boolean true" | debconf-set-selections
apt-get install iptables-persistent

### if user answers y|yes: forward ports ###
# TODO: set a flag on vm to initiate hostname resolution configs #
read -r -p "Do you want ports forwarded externally? [y/N] " response
response=${response,,}    # tolower
if [[ $response =~ ^(yes|y)$ ]]; then
	forward_ports
fi

## build metron ##
cd /
if [ ! -d /incubator-metron ]; then
	echo "cloning repo and building metron-vm.."
	git clone --recursive https://github.com/apache/incubator-metron
	cd /incubator-metron
else
	echo "pulling latest ver of metron"
	cd /incubator-metron
	git pull https://github.com/apache/incubator-metron.git
fi
# TODO: return code evals to non-zero even if succesful #
echo "compiling metron..."
cmnd=$(mvn clean install -PHDP-2.5.0.0 -DskipTests)
eval "${cmnd}"
ret_code=$?
if [ $ret_code != 0 ]; then
	printf "Error : [%d] when executing command: '$cmnd'" $ret_code
	exit $ret_code
else
	echo "metron compilation success"
fi
echo "installing metron vm on host.."
vagrant plugin install vagrant-hostmanager
cd /incubator-metron/metron-deployment/vagrant/quick-dev-platform
# change vm ram from 8GB => 16GB #
sed -i '48s/.*/    memory: "16384",/' Vagrantfile
echo "starting up metron vm.."
vagrant up
sleep 30

# setup vagrant configs and run cmds on vm #
METRON_VAGRANT_DIR=/incubator-metron/metron-deployment/vagrant/quick-dev-platform
echo "Vagrant Directory Used: $METRON_VAGRANT_DIR"

# Use the built-in environment variable to specify the Vagrantfile to use #
VAGRANT_VAGRANTFILE=$METRON_VAGRANT_DIR/Vagrantfile
echo "Vagrant File Used: $VAGRANT_VAGRANTFILE"

cd $METRON_VAGRANT_DIR
SSH_PRIVATE_KEY=`vagrant ssh-config | grep IdentityFile | awk '{print $2}'|sed 's/\"//g'`
echo "Vagrant SSH_PRIVATE_KEY:$SSH_PRIVATE_KEY"

# get host machine's current ip #
HOST_IP=$(ip route get 8.8.8.8 | awk 'NR==1 {print $NF}')
echo "Current IP address of host: $HOST_IP"
# TODO: add automation of setting env var in vagrant up cmd #
echo "HOST_IP=$HOST_IP" >> ~/.bashrc

# TODO: write permissions still denied by vm #
cd /threatdetectionservice/deploy
scp -r -P 2222 -i $SSH_PRIVATE_KEY assets-hosts asset-data capture-data scripts vagrant@127.0.0.1:/
# alternative scp cmd #
vagrant ssh -- -t <<- SCRIPT
    sudo -i
    yum -y install expect
	/usr/bin/expect <<- EOE
	set timeout 1
	spawn scp -r anon@$HOST_IP:/threatdetectionservice/deploy/\{assets-hosts,asset-data,capture-data,scripts,ojdbc6.jar\} /
	expect yes/no { send yes\r ; exp_continue }
	expect "password:" { send "$HOST_PW" }
	EOE
SCRIPT
if [ $? -eq 0 ]; then
	echo "File transfer successful."
	echo "Running config script on vm.."
	vagrant ssh -- -t <<- SCRIPT
    sudo -i
    exec /scripts/config.sh
SCRIPT
fi

# for security remove from memory #
unset HOST_PW

## set environment variables in ~/.bashrc on host & vm ##
echo "setting environment variables.."
# extract metron version from the pom
METRON_VERSION=`cat /incubator-metron/pom.xml | grep "<version>" | head -1 | sed -ne '/version/{s/.*<version>\(.*\)<\/version>.*/\1/p;q;}'`

echo "METRON_VERSION="${METRON_VERSION}""
echo "METRON_VERSION="${METRON_VERSION}"" >> ~/.bashrc

echo "METRON_VAGRANT_DIR=$METRON_VAGRANT_DIR"
echo "METRON_VAGRANT_DIR=$METRON_VAGRANT_DIR" >> ~/.bashrc
echo "alias qd=\"cd $METRON_VAGRANT_DIR\"" >> ~/.bashrc

echo "METRON_UI=node1:5000"
echo "METRON_UI=node1:5000" >> ~/.bashrc

echo "AMBARI_UI=node1:8080"
echo "AMBARI_UI=node1:8080" >> ~/.bashrc

echo "CLUSTER_NAME=metron_cluster"
echo "CLUSTER_NAME=metron_cluster" >> ~/.bashrc

echo "NIFI_HOST=node1:8089/nifi"
echo "NIFI_HOST=node1:8089/nifi" >> ~/.bashrc

echo "ZOOKEEPER_HOST=node1:2181"
echo "ZOOKEEPER_HOST=node1:2181" >> ~/.bashrc

echo "ZOOKEEPER_INFO=node1:16010/zk.jsp"
echo "ZOOKEEPER_INFO=node1:16010/zk.jsp" >> ~/.bashrc

echo "KAFKA_HOST=node1:6667"
echo "KAFKA_HOST=node1:6667" >> ~/.bashrc

echo "KAFKA_BROKER=node1:9092"
echo "KAFKA_BROKER=node1:9092" >> ~/.bashrc

echo "HBASE_UI=node1:16010/master-status"
echo "HBASE_UI=node1:16010/master-status" >> ~/.bashrc

echo "STORM_UI=node1:8744"
echo "STORM_UI=node1:8744" >> ~/.bashrc

echo "SEARCH_HOST=node1:9300"
echo "SEARCH_HOST=node1:9300" >> ~/.bashrc

echo "metron : metron bash cmd for convenience scripts"
echo 'PATH=$PATH:/threatdetectionservice/deploy/metron' >> ~/.bashrc

source ~/.bashrc

echo "setting environment variables in metron vm.."
vagrant ssh -- -t <<- SCRIPT
    sudo -i
    echo "METRON_VERSION=$METRON_VERSION" >> ~/.bashrc
    echo "METRON_HOME=/usr/metron/$METRON_VERSION" >> ~/.bashrc
    echo "HOST_IP=$HOST_IP" >> ~/.bashrc
    echo "METRON_UI=$METRON_UI" >> ~/.bashrc
    echo "AMBARI_UI=$AMBARI_UI" >> ~/.bashrc
    echo "CLUSTER_NAME=$CLUSTER_NAME" >> ~/.bashrc
    echo "NIFI_HOST=$NIFI_HOST" >> ~/.bashrc
    echo "ZOOKEEPER_HOST=$ZOOKEEPER_HOST" >> ~/.bashrc
    echo "ZOOKEEPER_INFO=$ZOOKEEPER_INFO" >> ~/.bashrc
    echo "KAFKA_HOST=$KAFKA_HOST" >> ~/.bashrc
    echo "KAFKA_BROKER=$KAFKA_BROKER" >> ~/.bashrc
    echo "HBASE_UI=$HBASE_UI" >> ~/.bashrc
    echo "STORM_UI=$STORM_UI" >> ~/.bashrc
    echo "SEARCH_HOST=$SEARCH_HOST" >> ~/.bashrc
    source ~/.bashrc
SCRIPT

echo "deployment process completed successfully"
exit 0
