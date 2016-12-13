#!/bin/bash
#########################################
# Name of the Script        : ddl.sh
# No. of Input Parameters   : 2
# Input Parameter accepted  : <command filepath> <table location in hbase> | e.g. createtables.sh /home/hadoop/ /home/hadoop/hbasem7/path/
# Comment                   : This shell script run all the commands present in command file param $1.
###########################################
usage() {
        echo "`date +%Y%m%d%H%M%S`: Usage: $0 <hbase command file> <table location>" 1>&2;
        exit 1;
}
if [ $# -ne 2 ]
then
        usage;
fi;
STATUS=0
file_path=$1
ip=$(echo ${2}| sed 's/\//\\\//g')
while read line;do
        command=$(echo ${line} | sed -e "s/#table_path#/${ip}/g")
        echo "executing command on hbase; ${command}"
        echo ${command}| hbase shell
        if [ "$?" != "0" ]; then
        echo "Error while creating tables" 1>&2
        STATUS=1;
fi
done <"${file_path}"
exit ${STATUS};

