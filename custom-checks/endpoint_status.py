# /bin/python
import sys
import boto
import boto.s3.connection
import ntpath
import socket
#import key
#from key import *
from ws_read_write_status import *

#TODO: rgw_instances should come from a config file
rgw_instances = ['https://dss.ind-west-1.staging.jiocloudservices.com']
#print rgw_instances

if(os.environ.has_key('http_proxy')):
    del os.environ['http_proxy']
if(os.environ.has_key('https_proxy')):
    del os.environ['https_proxy']
for rgw in rgw_instances:
    ws_read_write_status(rgw)

	
