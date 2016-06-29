#!/bin/python
#import csv
import os
import sys
f = open('./parsed_api.log','w')
data = []
valarray = []
#for var in {10}:
os.system("cp /var/log/api.log /var/log/api-copy.log")
infile = "/var/log/api-copy.log"
rtt = ''
reqdone="req done "
with open(infile) as f1: 
        f1 = f1.readlines()
for line in f1: 
        rtt =line
        mList= line.split(" ")
        out = mList[13:len(mList)]
	str1=''
	for i,x in enumerate(out):
            if i:  str1=str1+' '+str(x)
            else: str1=str1+str(x)
	f.write(str1)
	if str1.find(reqdone) !=-1 : f.write('\n')
os.system("rm -f /var/log/api-copy.log")

f.close()

