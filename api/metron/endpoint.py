from flask import jsonify, request
from flask_restful import Resource, reqparse
import requests
#from sql.models import *  #import all of the models from models.py
#from app.parse_json import * #for json arg parsing

metronElasticBaseURL="http://10.10.10.154:9200"
metronElasticIndex = "/bro_index_2016.10.27.22"
metronElasticVerb="/_search?"
metronElasticQuery="q=ip_dst_port:53"

metronElasticURL=metronElasticBaseURL + metronElasticIndex + metronElasticVerb + metronElasticQuery

class metronThreats(Resource):
    # update a company's info #
    def get(self, _device_):
        try:
            print(metronElasticURL)
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


if __name__ == '__main__':
    mt = metronThreats()
    print(mt.get('galzer'))
