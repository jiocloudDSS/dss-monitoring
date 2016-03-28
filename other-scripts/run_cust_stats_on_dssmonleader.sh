#!/bin/bash

time=`date +%s`
filename_all_stats=cust_stats_$time
filename_usr_stats=user_stats_$time

#copy scripts and customer ids

scp -i /home/obj_team/monitoring/id_rsa -o "StrictHostKeyChecking no" /home/obj_team/monitoring/get_cust_stats.sh obj_team@10.140.208.223:/tmp/

#run script
ssh -i /home/obj_team/monitoring/id_rsa -o "StrictHostKeyChecking no" obj_team@10.140.208.223 "sudo bash /tmp/get_cust_stats.sh /tmp/$filename_all_stats /tmp/$filename_usr_stats"

#copy results
scp -i /home/obj_team/monitoring/id_rsa -o "StrictHostKeyChecking no" obj_team@10.140.208.223:/tmp/$filename_all_stats /tmp/$filename_all_stats
#remove results and scripts
ssh -i /home/obj_team/monitoring/id_rsa -o "StrictHostKeyChecking no" obj_team@10.140.208.223 "sudo rm -f /tmp/$filename_all_stats /tmp/$filename_usr_stats /tmp/get_cust_stats.sh"
/usr/bin/mail -s "DSS production customer stats" -a "From: dssstats@ril.com" harshal.gupta@ril.com,shivanshu.goswami@ril.com,praveen.p.prakash@ril.com,gaurav.bafna@ril.com,rajat.garg@ril. com,abhishek.s.dixit@ril.com,rahul.aggarwal@ril.com <  /tmp/$filename_all_stats
sleep 10
rm -f /tmp/$filename_all_stats

