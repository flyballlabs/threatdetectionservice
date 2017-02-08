#!/usr/bin/python2.7

'''
@summary: Based on Flowroute Python SDK, a script for sending sms in python2.7
@author: devopsec

flowroute-messaging-python is a Python SDK that provides methods to send an outbound SMS from a Flowroute phone number
and also to retrieve a Message Detail Record (MDR). These methods use v2 (version 2) of the Flowroute API.
Copyright Flowroute, Inc.  2016
'''

import sys, pprint, argparse
sys.path.insert(0, ("/python/threatdetectionservice_test/api/notification"))
from flowroute.FlowrouteMessagingLib.Controllers.APIController import *
from flowroute.FlowrouteMessagingLib.Models.Message import *

# Parse cmd line args
parser = argparse.ArgumentParser(description='Send an sms message')
parser.add_argument('-t', '--to', type=str, dest='to_numbers',
                    help='Number (or) list of numbers to send sms to')
parser.add_argument('-f', '--from', type=str, dest='from_number', help='Number sms is from')
parser.add_argument('-m', '--msg', type=str, dest='msg_content', help='Content of sms message')
args = vars(parser.parse_args())

# convert string representation of int list to list
# args['to_numbers'] = args['to_numbers'].split(',')
print args['to_numbers']

# Set up your API credentials
# Please replace the variables in Configuration.php with your information.
username = '16723617'
password = 'd5db7e5c74b3c1768de8ee2910fc3aa2'

# Create the Controller
controller = APIController(username=username, password=password)
pprint.pprint(controller)

# Build your message
msg = args['msg_content']

# DEBUG
# print args['msg_content']

message = Message(to=args['to_numbers'], from_=args['from_number'], content=msg)

# Send your message
try:
    response = controller.create_message(message)
    pprint.pprint(response)
except APIException as e:
    print("Error - " + str(e.response_code) + '\n')
    pprint.pprint(e.response_body['errors'])
    raise SystemExit        # can't continue from here

# Get the MDR id from the response
mdr_id = response['data']['id']

# Retrieve the MDR record
try:
    mdr_record = controller.get_message_lookup(mdr_id)  # 'mdr1-b334f89df8de4f8fa7ce377e06090a2e'
    pprint.pprint(mdr_record)
except APIException as e:
    print("Error - " + str(e.response_code) + '\n')
    pprint.pprint(e.response_body['errors'])
