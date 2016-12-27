#!/usr/bin/python3.5

'''
@summary: Bootstrapper file to run rest_server, and flask api's associated with it.
Ensures all submodules are added to sys path and configures all runtime settings.
@author devopsec
'''

import os
from api import database;
from flask import Flask, make_response, jsonify, g, url_for ,abort, request
from flask_restful import Api  #, marshal, Resource, reqparse, fields
from flask_cors import CORS, cross_origin

# import endpoints #
from api.auth.endpoint import userAuth
from api.user.endpoint import manageUser, manageUserList
from api.agent.endpoint import piController, manageAgent, manageAgentList
from api.company.endpoint import manageCompany, manageCompanyList
from api.asset.endpoint import manageAssets
from api.metron.endpoint import metronThreats
#from api.notification.endpoint import manageNotifications
#from api.metron_data.endpoint import asset_discovery, threat_intel

# flask / sql / api config  #
app = Flask('rest_server')
#app.config['DEBUG'] = False
api = Api(app)
CORS(app)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


api.add_resource(metronThreats, '/api/metron/threats/<string:_device_>')
api.add_resource(manageAssets, '/api/assets', '/api/assets/<string:_company_name_>/<string:_sites_>/<string:_asset_ip_>') #'/api/assets/<string:_company_name_>', '/api/assets/<string:_company_name_>/<string:_sites_>',

api.add_resource(piController, '/api/picontroller/time', '/api/picontroller/<string:_mac_address_>')
api.add_resource(manageAgent, '/api/agent/<string:_mac_address_>')
api.add_resource(manageAgentList, '/api/agent/list')

api.add_resource(userAuth, '/api/auth/<string:_username>/<string:_password>')
api.add_resource(manageUser, '/api/user/<string:_username_>')
api.add_resource(manageUserList, '/api/user/list')

api.add_resource(manageCompany, '/api/company/<string:_company_name_>')
api.add_resource(manageCompanyList, '/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites',
'api/company/poc', '/api/company/<string:_company_name_>/poc')

#api.add_resource(manageNotifications, '/api/notification', '/api/notification/<string:_username_>')
#api.add_resource(threat_intel, '/api/metron_data/threat_intel', '/api/metron_data/threat_intel/<string:_company_name_>', '/api/metron_data/threat_intel/<string:_company_name_>/<string:_sites_>')
                 
if __name__ == '__main__':
    if not os.path.exists('db.mysql'):
        db = connect()
        db.create_all()
    app.run(host='0.0.0.0', port=7777, debug=True)
