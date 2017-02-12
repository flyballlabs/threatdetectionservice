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
	exit

}

if [ -z ${PYTHON_CMD+x} ]; then
	isPythonInstalled
fi
$PYTHON_CMD api/rest_server.py
