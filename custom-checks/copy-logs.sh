#!/bin/bash
pattern=$1
rgw_file=$2
key_path=$3

for var in $(cat $rgw_file) 
do
    echo "searching for pattern $pattern"
    arr=($(ssh -i $key_path obj_team@$var "ls /var/log/ceph/radosgw.*"))
    for log in "${arr[@]}"
    do  
        echo "checking $log file"
        basefile=`basename $log`
        ssh -i ${key_path} obj_team@$var "zgrep '${pattern}' '${log}'"
        if [ "$?" -eq 0 ];
        then
            echo "copying $log file"
            scp -i ${key_path} obj_team@$var:${log} ./"${basefile}-${var}"
        fi

    done
done
