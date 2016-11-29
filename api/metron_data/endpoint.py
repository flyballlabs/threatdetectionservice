from flask import jsonify, request
from flask_restful import Resource, reqparse
import requests, json, base64
from api.sql.models import *  #import all of the models from models.py
from api.app.parse_json import * #for json arg parsing
from collections import OrderedDict

'''
# Method for encoding ints with base64 encoding
def encode(n):
     data = struct.pack("i", n)
     s = base64.b64encode(data)
     return s
 
# Method for decoding ints with base64 encoding
def decode(s):
     data = base64.b64decode(s)
     n = struct.unpack("i", data)
     return n[0]
    
# Checks the request object to see if the call was successful
def issuccessful(request):
    if 200

# check if table exists #
def checkTable():
    request = requests.get(hbaseBaseURL + "/" + hbaseTableName + "/schema")

# delete table #
def deleteTable():
    request = requests.delete(hbaseBaseURL + "/" + hbaseTableName + "/schema")
########

hbaseBaseURL="http://10.10.10.154:9082"
hbaseTableName = "enrichment"
hbaseSiteName = "glazer-*"

request = requests.get(hbaseBaseURL + "/" + hbaseTableName + "/" + hbaseSiteName, headers={"Accept" : "application/json"})

class metronThreats(Resource):
    # update a company's info #
    def get(self, _device_):
        try:
            print(request)
            bleats = json.loads(request.text)
     
            for row in bleats['Row']:
                message = ''
                lineNumber = 0
                username = ''
             
                for cell in row['Cell']:
                    columnname = base64.b64decode(cell['column'])
                    value = cell['$']
                     
                    if value == None:
                        continue
             
                    if columnname == hbaseCFName + ":" + messagecolumn:
                        message = base64.b64decode(value)
                    elif columnname == hbaseCFName + ":" + linenumbercolumn:
                        lineNumber = decode(str(value))
                    elif columnname == hbaseCFName + ":" + usernamecolumn:
                        username = base64.b64decode(value)
             
                rowKey = base64.b64decode(row['key'])
            
            response = requests.get(metronElasticURL)
            jData = response.json()
            #data = [{ 'id': 1, 'threatlevel': 2, 'incidenttype': 'Out of Country Access' }]
        #data['id'] = 1
            #data['threatlevel'] = 2
            #data['incidenttype'] = 'Out of Country Access'
        
            #Just return the hits and then we will filter
            hits = jData['hits']['hits']
            return jsonify(hits)

        except:
            return "Server Down"

def post():
    rows = []
    jsonOutput = { "Row" : rows }
     
    for line in shakespeare:
        rowKey = username + "-" + filename + "-" + str(lineNumber).zfill(6)
        rowKeyEncoded = base64.b64encode(rowKey)
     
        line = base64.b64encode(line.strip())
        lineNumberEncoded = encode(lineNumber)
        usernameEncoded = base64.b64encode(username)
     
        cell = OrderedDict([
            ("key", rowKeyEncoded),
            ("Cell",
            [
                { "column" : messagecolumnencoded, "$" : line },
                { "column" : usernamecolumnencoded, "$" : usernameEncoded },
                { "column" : linenumbercolumnencoded, "$" : lineNumberEncoded },
            ])
        ])
     
        rows.append(cell)
     
        lineNumber = lineNumber + 1
     
    # Submit JSON to REST server
    request = requests.post(hbaseBaseURL + "/" + hbaseTableName + "/" + rowKey, data=json.dumps(jsonOutput), headers={"Content-Type" : "application/json", "Accept" : "application/json"})

'''
class asset_discovery(object):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('asset_id', type=int, help='Asset_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Company Name that owns asset', location='json')
            parser.add_argument('site', type=str, help='Site where asset is located', location='json')
            parser.add_argument('asset_ip', type=str, help='Asset IP Address', location='json')
            parser.add_argument('asset_mac', type=str, help='MAC Address', location='json')
            parser.add_argument('asset_type', type=str, help='Type of asset deployed', location='json')
            parser.add_argument('asset_os', type=str, help='Os running on asset', location='json')
            parser.add_argument('asset_os_info', type=str, help='Extended os info', location='json')
            args = parser.parse_args()#strict=True

            _asset_id = args['asset_id']
            _company_name = args['company_name']
            _site = args['site']
            _asset_ip = args['asset_ip']
            _asset_mac = args['asset_mac']
            _asset_type = args['asset_type']
            _asset_os = args['asset_os']
            _asset_os_info = args['asset_os_info']
            
            query = user_data(asset_id=_asset_id, company_name=_company_name, site=_site, asset_ip=_asset_ip, asset_mac=_asset_mac,
                            asset_type=_asset_type, asset_os=_asset_os, asset_os_info=_asset_os_info)

            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                            'status': 200,
                            'message':'Asset creation successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status': 400,
                            'message':'Asset creation failure'
                        }
        except Exception as e:
            return {'error': str(e)}

'''
class threat_intel(object):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int, help='User_id for account', location='json')
            parser.add_argument('username', type=str, help='Username for account', location='json')
            parser.add_argument('firstname', type=str, help='Firstname for account', location='json')
            parser.add_argument('lastname', type=str, help='Lastname for account', location='json')
            parser.add_argument('password', type=str, help='Password for account', location='json')
            parser.add_argument('email', type=str, help='Email for account', location='json')
            parser.add_argument('company_id', type=str, help='Company_id for account', location='json')
            parser.add_argument('status', type=str, help='Status for account', location='json')
            parser.add_argument('lastlogin', type=str, help='Lastlogin for account', location='json')
            args = parser.parse_args()#strict=True

            _user_id = args['user_id']
            _username = args['username']
            _firstname = args['firstname']
            _lastname = args['lastname']
            _password = args['password']
            _email = args['email']
            _company_id = args['company_id']
            _status = args['status']
            _lastlogin = args['lastlogin']
            
            query = user_data(user_id=_user_id, username=_username, firstname=_firstname, 
                              lastname=_lastname, password=_password, email=_email, 
                              company_id=_company_id, status=_status, lastlogin=_lastlogin)

            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                            'status': 200,
                            'message':'User creation successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status': 400,
                            'message':'User creation failure'
                        }
        except Exception as e:
            return {'error': str(e)}
'''