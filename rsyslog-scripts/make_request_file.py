import os
import sys
import time
import subprocess

inputbucks = raw_input("Enter the request id:" ).split()
request_id = inputbucks[0]
print request_id
filename="/var/log/filtered_rsyslog.log"
command= "cat /var/log/filtered_rsyslog.log | grep "+request_id
call=os.popen(command).read()
#call=os.system(command)
#call = str(call)
print call
lines = call.split()
#lines = int(lines)
threadid=lines[7]
print threadid
#startStr = threadid+"  1 DSS INFO: Num headers is:"
#print startStr
command="sed -n -e '/"+request_id+"/,/"+request_id+"/ p' "+filename
jumbledoutput=os.popen(command).read()
print jumbledoutput
f= open('buffer.log', 'w')
f.write(jumbledoutput)
f.close()
command = "cat buffer.log | grep "+threadid
call=os.popen(command).read()
f1 = open('result.log', 'w')
f1.write(call)
f1.close()
