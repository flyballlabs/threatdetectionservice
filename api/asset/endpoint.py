''' @Summary: API endpoint to access asset data from hbase database '''

from flask import jsonify, request, json
from flask_restful import Resource, reqparse
import base64, requests

#from sql.models import *  #import all of the models from models.py
#from app.parse_json import * #for json arg parsing

#TODO: determine if we want data in both db's or just hbase
#TODO: finish asset posts, puts and deletes functionality

metronHBaseRestURL="http://10.10.10.154:9082"
metronHBaseTable = "enrichment"
metronHBaseCF="assets"
assetSearch = ""

assetQueryURL =metronHBaseRestURL + "/" + metronHBaseTable 

class manageAssets(Resource):
    # update a company's info #
    def get(self, _device_):
        #Lookup Company
        company = "Flyball-Labs"
        assetSearch = company + "_" + _device_ + "_*"
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

               


if __name__ == '__main__':
    mt = manageAssets()
    print(mt.get('glazer'))
