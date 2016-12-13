'''
@description: This endpoint holds logic for accessing asset data from hbase
'''

from flask import jsonify, request, json
from flask_restful import Resource, reqparse
from starbase import Connection
import requests, base64
#from sql.models import *  #import all of the models from models.py
#from app.parse_json import * #for json arg parsing

metronHBaseRestURL="http://10.10.10.154"
metronHbaseRestPort = 9082
metronHBaseTable = "enrichment"
metronHBaseCF="assets"
assetSearch = ""

assetQueryURL =metronHBaseRestURL + ":" + str(metronHbaseRestPort) + "/" + metronHBaseTable 

class manageAssets(Resource):
    
    def get(self, _company_name_, _sites_, _mac_address_):
        assetSearch = _company_name_ + "_" + _sites_ + "_" + _mac_address_
        assetFullQueryURL = assetQueryURL + "/" + assetSearch
        print(assetFullQueryURL)
        try:
            response = requests.get(assetFullQueryURL, headers={"Accept" : "application/json"})
            jData = response.json()
        except:
            return "Server Down"
        counter = 0
        decodedList  = []
        for row in jData['Row']:
            # Decode the key into ascii
            #rowKey = base64.b64decode(row['key']).decode('ascii')
            dColumn = {}
            for cell in row['Cell']:
                columnname = base64.b64decode(cell['column']).decode('ascii')
                value = base64.b64decode(cell['$']).decode('ascii')
                dColumn[columnname] = value 
            decodedList.append (dColumn) 
        return jsonify(decodedList)
    
    ## shema for rowkey: companyname_site_ipaddress ##
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('company_name', type=str, location='json')
            parser.add_argument('site', type=str, location='json')
            parser.add_argument('asset_ip', type=str, location='json')
            parser.add_argument('asset_mac', type=str, location='json')
            parser.add_argument('asset_type', type=str, location='json')
            parser.add_argument('asset_os', type=str, location='json')
            parser.add_argument('asset_os_info', type=str, location='json')
            args = parser.parse_args()#strict=True
            
            _company_name = args['company_name']
            _site = args['site']
            _asset_ip = args['asset_ip']
            _asset_mac = args['asset_mac']
            _asset_type = args['asset_type']
            _asset_os = args['asset_os']
            _asset_os_info = args['asset_os_info']
            
            rowkey = _company_name + "_" + _site + "_" + _asset_ip

            try:
                c = Connection(host=metronHBaseRestURL, port=metronHbaseRestPort)
                t = c.table(metronHBaseTable) #create table object in memory      
                if t.exists() == True:
                    #t.disable_row_operation_if_exists_checks()
                    t.insert(rowkey,{metronHBaseCF:  {
                                                    'asset_ip': _asset_ip,
                                                    'asset_mac': _asset_mac,
                                                    'asset_type': _asset_type,
                                                    'asset_os': _asset_os,
                                                    'asset_os_info': _asset_os_info
                                                }})
                
                return  {
                            'status': 200,
                            'message':'Asset creation successful'
                        }
            except Exception as ex:
                return  {
                            'status': 400,
                            'message':'Asset creation failure'
                        }
        except Exception as e:
            return {'error': str(e)}
            

#             t.update(
#                 'my-key-1',
#                 {'column4': {'key41': 'value 41', 'key42': 'value 42'}}
#                 )
#             
#             t.fetch('my-key-1')
            ### list tables ###
            #c.tables() #output: ['table1', 'table2']
            ### create new table ###
            #t.create('column1', 'column2') #output: 201
            ### show table columns ###
            #t.columns() #output: ['column1', 'column2']
            ### add columns to a table ###
            #t.add_columns('column3', 'column4', 'column5') #output: 200
            ### drop columns from table ###
            #t.drop_columns('column3', 'column4') #output: 201
            ### drop table schema (table object) ###
            #t.drop() #output: 200