#!/bin/bash

REQ_PYTHON_VER=3.5

# Uncomment and set this variable to an explicit Python executable file name
# If set, the script will not try and find a Python version with 3.5 as the major release number
# PYTHON_CMD=/usr/local/python3.5

function isPythonInstalled {

possible_python_versions=`find / -name "python*" -type f -executable  2>/dev/null`
for i in $possible_python_versions
do
        ver=`$i -V 2>&1`
        echo $ver | grep $REQ_PYTHON_VER >/dev/null
        if [ $? -eq 0 ]; then
                PYTHON_CMD=$i
                return
        fi
done

#Required version of Python is not found.  So, tell the user to install the required version
        echo -e "\nPlease install at least python version $REQ_PYTHON_VER\n"
        exit 1
}

function installServerDependencies {
    echo "installing server dependencies.."

    if uname -a | grep -i "linux"; then
        DEBIAN_FRONTEND=noninteractive apt-get update
		DEBIAN_FRONTEND=noninteractive apt-get install python-setuptools python-pip python3-pip build-essential python-dev
        yes | pip install --upgrade pip
        DEBIAN_FRONTEND=noninteractive apt-get install uwsgi uwsgi-emperor uwsgi-plugin-python3 nginx-full tshark
    elif uname -a | grep -i "mac"; then
        if ! whichapp 'homebrew' &>/dev/null; then
            echo "installing homebrew.."
            /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        fi

        echo "updating homebrew.."
        brew upgrade
        brew update

        if ! whichapp 'uwsgi' &>/dev/null; then
            echo "installing uwsgi.."
            brew install uwsgi
        fi

        if ! whichapp 'nginx' &>/dev/null; then
            echo "installing nginx.."
            brew install nginx
        fi
    fi
}

if [ -z ${PYTHON_CMD+x} ]; then
        isPythonInstalled
        installServerDependencies
fi

$PYTHON_CMD -m pip install -r ./api/requirements.txt

sleep 1 # ensure pip is finished
exit 0
