from flask import jsonify, request, json
from flask_restful import Resource, reqparse
import requests
import base64

#from sql.models import *  #import all of the models from models.py
#from app.parse_json import * #for json arg parsing

metronHBaseRestURL="http://10.10.10.154:9082"
metronHBaseTable = "enrichment"
metronHBaseCF="assets"
assetSearch = ""

assetQueryURL =metronHBaseRestURL + "/" + metronHBaseTable 

class manageAssets(Resource):
    # update a company's info #
    def get(self, _device_):
        assetSearch = _device_ + "-*"
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
