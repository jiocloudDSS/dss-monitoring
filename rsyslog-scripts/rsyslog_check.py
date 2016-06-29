import os
import sys
import time
import subprocess
from datetime import datetime

filename='/var/log/filtered_rsyslog.log'
filename1='/var/log/ceph/radosgw.log'
FMT = '%H:%M:%S'
#filename="/home/obj_team/log_tests/imux"
command = "grep imuxsock "+filename
call=os.popen(command).read()
strippedString = call.strip()
if strippedString:
	print "Unexpected imuxsock present in log => there might be a drop in packets"
	print strippedString
else:
	print "packet drop test passed"



'''	
command = "tail -1 "+filename
call=os.popen(command).read()
tokens = call.split()
s2=tokens[2]
#s2 = '12:12:12'
command = "date"
call=os.popen(command).read()
tokens = call.split()
s1=tokens[3]

delta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)

if  delta.seconds > 1:
	print "Centralized log is not populated correctly : FAILED"
	print delta
else:
	print "Logs update correctly : PASSED"
'''
	
command = "logger test_message"
call=os.popen(command).read()

command = "cat /var/log/syslog | grep test_message"
call=os.popen(command).read()
strippedString = call.strip()
if strippedString:
	print "Expected test_message present in log : PASSED"
	print strippedString
else:
	print "Is rsyslog working test : FAILED"


print "Calculating logs on central server"
reqdone = "'====== req done'"
sshstr="\"sudo grep "+reqdone+ " "+filename+" | wc -l\""
command = "ssh -i ../rahul_id_rsa obj_team@10.140.222.33 "+ sshstr 
numreqs_completed = os.popen(command).read()
print numreqs_completed

reqstart = "'====== starting'"
sshstr = "\"sudo grep "+reqstart+ " "+filename+" | wc -l\""
command = "ssh -i ../rahul_id_rsa obj_team@10.140.222.33 "+ sshstr 
numreqs_started = os.popen(command).read()
print numreqs_started 

if numreqs_completed == numreqs_started:
	print "Complete requests logged test: PASSED"
else:
	print "Complete requests logged test: FAILED"

########### Change this line only for changing the radosgw on which test (log has to e counted) has to be run#######
clients=["10.140.214.196", "10.140.214.197"]

reqs_completed = 0
reqs_started = 0
for client in clients:
  reqdone = "'====== req done'"
  sshstr="\"sudo grep "+reqdone+ " "+filename1+" | wc -l\""
  command = "ssh -i ../rahul_id_rsa obj_team@"+client+" "+ sshstr 
  numreqs_completed = os.popen(command).read()
  print "completed requests for "+client+" :: "+numreqs_completed
  reqs_completed += int(numreqs_completed)

  reqstart = "'====== starting'"
  sshstr = "\"sudo grep "+reqstart+ " "+filename1+" | wc -l\""
  command = "ssh -i ../rahul_id_rsa obj_team@"+client+" "+ sshstr 
  numreqs_started = os.popen(command).read()
  print "completed started for "+client+" :: "+numreqs_started
  reqs_started += int(numreqs_started)
  	
#print numreqs_completed
#print numreqs_started 

print reqs_completed
print reqs_started
