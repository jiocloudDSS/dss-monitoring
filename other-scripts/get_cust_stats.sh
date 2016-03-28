#!/bin/bash
filename_all_stats=$1
filename_usr_stats=$2
for line in `sudo radosgw-admin metadata list user | grep \\" | sed 's/ *"//g' | sed 's/,//g'`; do
    account_id=$line
    #echo "User : $line"
    #echo "$account_id"
    #echo $account_name
    echo "radosgw-admin user stats --uid=$account_id"
    echo "" >> $filename_all_stats
    echo "" >> $filename_all_stats
    echo "" >> $filename_all_stats
    echo "================================================================================" >> $filename_all_stats
    echo "Stats for user : $line" >> $filename_all_stats
    #echo "Buckets" >> $filename_all_stats
    num_buckets=`sudo radosgw-admin bucket list --uid=$account_id |  grep \\" | wc -l`
    #echo "====================== $num_buckets"
    echo "Number of buckets : $num_buckets" >> $filename_all_stats
    echo "Objects" >> $filename_all_stats
    sudo radosgw-admin user stats --uid=$account_id 2> /dev/null > $filename_usr_stats
    cat $filename_usr_stats >> $filename_all_stats
    #echo "================================================================================" >> $filename_all_stats
done 

