#!/usr/bin/python2.7

'''
flowroute-messaging-python is a Python SDK that provides methods to send an outbound SMS from a Flowroute phone number
and also to retrieve a Message Detail Record (MDR). These methods use v2 (version 2) of the Flowroute API.
Copyright Flowroute, Inc.  2016
'''
import sys
sys.path.insert(0, ("/home/anon/eclipse/liclipse/workspace/threatdetectionservice_test/api/notification"))
from flowroute.FlowrouteMessagingLib.Controllers.APIController import *
from flowroute.FlowrouteMessagingLib.Models.Message import *
import pprint

# Set up your API credentials
# Please replace the variables in Configuration.php with your information.
username = '16723617'
password = 'd5db7e5c74b3c1768de8ee2910fc3aa2'

# Create the Controller
controller = APIController(username=username, password=password)
pprint.pprint(controller)

# Build your message
from_number = '12485042987'
to_number = '12489092769'
sender_list = []

message = Message(to=to_number, from_=from_number, content='Your cool new SMS message here!')

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
