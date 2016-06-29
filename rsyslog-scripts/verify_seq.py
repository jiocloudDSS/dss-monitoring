
import os
import sys
import time
import subprocess
from datetime import datetime

filename='/home/obj_team/log_tests/filtered_rsyslog.log'

command= "grep \"LOGGING: Request-Id:\" filtered_rsyslog.log"
numreqs_completed = os.popen(command).read()
iter1 = numreqs_completed.splitlines()
dd = {}
for line in iter1:
	mList= line.split(" ")
    # This is the server name in central log
	key = mList[3]
	# Extracting the trans id
	transid = mList[14].split("-")
	#transid = num.split("-")
	transid = transid[0][2:]
	transid = transid.lstrip("0")
	print transid
	try:
		print dd[key]
	except:
		dd[key] = transid
 		continue
		
	prev_transid = dd[key]
	num = int(prev_transid, 16) + 1
	predKey=hex(num)[2:]
	if (predKey) != (transid):
		print "Error: as logs might have dropped for radosgw "+key
		print predKey
		print transid
		exit()
	dd[key] = transid 

    


	print key
	print dd[key]

