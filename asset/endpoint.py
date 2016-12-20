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
    
    ## shema for row-key: companyname_site_ipaddress ##
    def post(self, _company_name_, _sites_):
        ##t.insert('row1',{'assets':{'hostname':'glazer','ip':'0.0.0.0'}})##
        c = Connection(host=metronHBaseRestURL, port=metronHbaseRestPort)
        t = c.table(metronHBaseTable) #create table object in memory      
        if t.exists() == True:
            t.insert(
                'my-key-1',
                {
                    'column1': {'key11': 'value 11', 'key12': 'value 12',
                                'key13': 'value 13'},
                    'column2': {'key21': 'value 21', 'key22': 'value 22'},
                    'column3': {'key32': 'value 31', 'key32': 'value 32'}
                }
                )
            
            t.insert(
                'my-key-1',
                {
                    'column1:key11': 'value 11', 'column1:key12': 'value 12',
                    'column1:key13': 'value 13',
                    'column2:key21': 'value 21', 'column2:key22': 'value 22',
                    'column3:key32': 'value 31', 'column3:key32': 'value 32'
                }
                )
            
            
            t.update(
                'my-key-1',
                {'column4': {'key41': 'value 41', 'key42': 'value 42'}}
                )
            
            t.fetch('my-key-1')
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