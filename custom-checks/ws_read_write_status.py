# /bin/python
import sys
import boto
import boto.s3.connection
import ntpath
import socket
import os
from key import *

#TODO: manage access and secret keys using environment variables

def ws_read_write_status(rgw):

    hostname = socket.gethostname()
    monitoring_bucket_name = 'dss.jcs.staging.monitoring.' + hostname + '.' + rgw 
    monitoring_object_name = 'dummy_object_' + hostname + '.' + rgw

	# create connection
    if(rgw.startswith('https')):
        rgw = rgw.replace('https://','')
        conn = boto.connect_s3(aws_access_key_id = access_key,
	                            aws_secret_access_key = secret_key,
	                            #port=443,
	                            host = rgw,
	                            is_secure=True,
                                validate_certs=False,
	                            calling_format = boto.s3.connection.OrdinaryCallingFormat())
    else:
        conn = boto.connect_s3(aws_access_key_id = access_key,
	                            aws_secret_access_key = secret_key,
	                            port=7480,
	                            host = rgw, 
	                            is_secure=False, 
	                            calling_format = boto.s3.connection.OrdinaryCallingFormat())

    
    
    monitoring_bucket_name = monitoring_bucket_name.replace('https://','').replace('-','.')
    monitoring_object_name = monitoring_object_name.replace('https://','').replace('-','.')

	# if bucket already exists delete it
    try:	
        for bucket in conn.get_all_buckets():
	        bucket_name = bucket.name
	        if(monitoring_bucket_name == bucket_name):
	            # delete all objects and delete bucket
	            for key in bucket.list():
	                object_name = key.name
	                bucket.delete_key(object_name)
	        
	        conn.delete_bucket(bucket_name)
	
    except:
        # do nothing
        e = sys.exc_info()[0]
    monitoring_bucket_name = monitoring_bucket_name.replace('-','')
    
    # create bucket
    status = '0'
    status_txt = 'OK'
    status_string = ''
    try:
        bucket = conn.create_bucket(monitoring_bucket_name)
        status = '0'
        status_txt = 'OK'
        status_string = 'Succesfully created bucket ' + monitoring_bucket_name
        print status + ' radosgw_create_bucket_' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'CREATE_BUCKET PASS ' + rgw
    except: 
        e = sys.exc_info()[1]
        msg = str(e).replace('\n', ' ').replace('\r', '')
        status = '2'
        status_txt = 'CRITICAL'
        status_string = msg
        print status + ' radosgw_create_bucket_' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'CREATE_BUCKET FAIL ' + rgw + ' ' + msg
	
    
    # write object
    try:
        key = bucket.new_key(monitoring_object_name)
        key.set_contents_from_string('I am monitoring object written from '  + hostname + ' to ' + rgw)
        status = '0'
        status_txt = 'OK'
        status_string = 'Succesfully put object ' + monitoring_object_name
        print status + ' radosgw_put_object' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'PUT_OBJECT PASS ' + rgw
    except: 
        e = sys.exc_info()[1]
        msg = str(e).replace('\n', ' ').replace('\r', '')
        status = '2'
        status_txt = 'CRITICAL'
        status_string = msg
        print status + ' radosgw_put_object_' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'PUT_OBJECT FAIL ' + rgw + ' ' + msg
	
    
    #read object 
    try:
        key = bucket.get_key(monitoring_object_name)
        contents = key.get_contents_as_string()
        #print contents
        status = '0'
        status_txt = 'OK'
        status_string = 'Succesfully read object ' + monitoring_object_name
        print status + ' radosgw_get_object' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'GET_OBJECT PASS ' + rgw
    except: 
        e = sys.exc_info()[1]
        msg = str(e).replace('\n', ' ').replace('\r', '')
        status = '2'
        status_txt = 'CRITICAL'
        status_string = msg
        print status + ' radosgw_get_object_' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'GET_OBJECT FAIL ' + rgw + ' ' + msg
	
    
    # delete object
    try:
        bucket.delete_key(monitoring_object_name)
        status = '0'
        status_txt = 'OK'
        status_string = 'Succesfully deleted object ' + monitoring_object_name
        print status + ' radosgw_del_object' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'DELETE_OBJECT PASS ' + rgw
    except: 
        e = sys.exc_info()[1]
        msg = str(e).replace('\n', ' ').replace('\r', '')
        status = '2'
        status_txt = 'CRITICAL'
        status_string = msg
        print status + ' radosgw_del_object_' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'DELETE_OBJECT FAIL ' + rgw + ' ' + msg

	# delete bucket
    try:
        conn.delete_bucket(monitoring_bucket_name)
        status = '0'
        status_txt = 'OK'
        status_string = 'Succesfully deleted bucket ' + monitoring_bucket_name
        print status + ' radosgw_del_bucket' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'DELETE_BUCKET PASS ' + rgw
    except: 
        e = sys.exc_info()[1]
        msg = str(e).replace('\n', ' ').replace('\r', '')
        status = '2'
        status_txt = 'CRITICAL'
        status_string = msg
        print status + ' radosgw_del_bucket_' + rgw + ' - ' + hostname + ' : ' + status_txt + ' - ' + status_string
        #print 'DELETE_BUCKET FAIL ' + rgw + ' ' + msg
	
