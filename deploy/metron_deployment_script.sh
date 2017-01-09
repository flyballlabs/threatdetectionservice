#!/bin/bash
# Author: devopsec
# Summary: Deployment script for metron to config vars and files.
# Note: This script must be run as root user to work properly.
# Note: Platform must be a unix-based x64 architecture os.

cd /

# function to install Oracle JDK & JRE and set paths for vars
function install_java {	
	echo "installing oracle java.."	
	add-apt-repository ppa:webupd8team/java
	apt-get update
	apt-get install oracle-java8-installer
	apt-get install oracle-java8-set-default
	echo 'JAVA_HOME="/usr/lib/jvm/java-8-oracle"' >> /etc/hosts;
	echo 'JRE_HOME="/usr/lib/jvm/java-8-oracle/jre' >> /etc/hosts;
	echo 'PATH=/apache-maven-3.3.9/bin:$JAVA_HOME/bin:$JRE_HOME/bin:$PATH' >> /etc/hosts;
	echo 'export JAVA_HOME' >> /etc/hosts;
	echo 'export JRE_HOME' >> /etc/hosts;
	echo 'export PATH' >> /etc/hosts;
	source /etc/profile
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
		apt-get purge openjdk-\*
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

# install dependencies if not already
if uname -a | grep -i "linux"; then
	TEMP=$(dpkg -l "ansible" 2>&1 | grep -i "no packages found")
	TEMP2=$(pip list 2>&1 | grep -i "ansible")
	if [[ -n "$TEMP" ]] && [[ -z "$TEMP2" ]]; then
		echo "installing ansible.."
		apt-get install software-properties-common
		apt-add-repository ppa:ansible/ansible
		apt-get update
		apt-get install ansible
	fi
	ansible --version

	TEMP=$(python --version 2>&1 | grep "2.7")
	if [[ -n "$TEMP" ]]; then
		echo "Python version: "${TEMP}""
	else
		echo "installing python.."
		apt-add-repository ppa:fkrull/deadsnakes-python2.7
		apt-get update
		apt-get install python2.7 python2.7-dev python-pip python-dev build-essential
		pip install --upgrade pip
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
		dpkg -i ~/Downloads/vagrant_1.9.1.deb
		apt-get install -f ~/Downloads/vagrant_1.9.1.deb
		vagrant --version
	fi

	TEMP=$(dpkg -l "virtualbox" 2>&1 | grep -i "no packages found")
	if [[ -n "$TEMP" ]]; then
		echo "installing virtualbox.."
		apt-get install dkms
		wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
		wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -
		echo "deb http://download.virtualbox.org/virtualbox/debian Yakkety contrib" >> /etc/apt/sources.list
		apt-get update
		apt-get install virtualbox-5.1
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

# build metron
cd /
if [ ! -d /tmp/mydir ]; then
	echo "cloning repo and building metron-vm.."
	git clone --recursive https://github.com/apache/incubator-metron
	cd /incubator-metron
else
	echo "pulling latest ver of metron"
	cd /incubator-metron
	git pull https://github.com/apache/incubator-metron.git
fi
echo "compiling metron vm.."
cmnd=$(mvn clean install -PHDP-2.5.0.0 -DskipTests)
eval "${cmnd}"
ret_code=$?
if [ $ret_code != 0 ]; then
printf "Error : [%d] when executing command: '$cmnd'" $ret_code
exit $ret_code
fi
vagrant plugin install vagrant-hostmanager
cd /incubator-metron/metron-deployment/vagrant/quick-dev-platform
vagrant up
cat /deploy/vm_deployment_script.sh | vagrant ssh

## set environment variables ##
echo "setting environment variables.."
# extract metron version from the pom
METRON_VERSION=`cat /incubator-metron/pom.xml | grep "<version>" | head -1 | sed -ne '/version/{s/.*<version>\(.*\)<\/version>.*/\1/p;q;}'`
echo "METRON_VERSION="${METRON_VERSION}""
echo "METRON_VERSION="${METRON_VERSION}"" >> ~/.bashrc

echo "METRON_HOME=/usr/metron/"${METRON_VERSION}""
echo "METRON_HOME=/usr/metron/"${METRON_VERSION}"" >> ~/.bashrc

echo "METRON_UI=node1:5000"
echo "METRON_UI=node1:5000" >> ~/.bashrc

echo "AMBARI_UI=node1:8080"
echo "AMBARI_UI=node1:8080" >> ~/.bashrc

echo "METRON_UI=node1:5000"
echo "METRON_UI=node1:5000" >> ~/.bashrc

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

echo "AMBARI_HOST=node1:8080"
echo "AMBARI_HOST=node1:8080" >> ~/.bashrc

echo "STORM_UI=node1:2812"
echo "STORM_UI=node1:2812" >> ~/.bashrc

echo "SEARCH_HOST=node1:9300"
echo "SEARCH_HOST=node1:9300" >> ~/.bashrc

echo "metron = metron bash cmd"
echo 'PATH=$PATH:/threatdetectionservice/deploy/metron' >> ~/.bashrc
source ~/.bashrc


