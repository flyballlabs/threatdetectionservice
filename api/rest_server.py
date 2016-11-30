#!/usr/bin/python3.5

'''
@summary: Bootstrapper file to run rest_server, and flask api's associated with it.
Ensures all submodules are added to sys path and configures all runtime settings.
@author devopsec
'''

from api import app;
from flask import Flask, make_response, jsonify #, request, abort, render_template, Flask
from flask_restful import Api #, reqparse, fields , marshal, Resource
from werkzeug.serving import run_simple

# import endpoints #
from api.auth.endpoint import userAuth
from api.user.endpoint import manageUsers
from api.agent.endpoint import manageAgents, piController
from api.company.endpoint import manageCompany, companyList
#from api.notification.endpoint import manageNotifications
from api.metron_data.endpoint import asset_discovery#, threat_intel


# flask / sql / api config  #
app = Flask('rest_server')
api = Api(app)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

api.add_resource(manageAgents, '/api/agent', '/api/agent/<string:_mac_address_>')
api.add_resource(piController, '/api/picontroller', '/api/picontroller/<string:_mac_address_>')
api.add_resource(userAuth, '/api/auth/<string:_username>/<string:_password>')
api.add_resource(manageUsers, '/api/user', '/api/user/<string:_username_>')
api.add_resource(manageCompany, '/api/company/<string:_company_name_>')
api.add_resource(companyList, '/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites')
#api.add_resource(manageNotifications, '/api/notification', '/api/notification/<string:_username_>')
#api.add_resource(asset_discovery, '/api/metron_data/asset_discovery', '/api/metron_data/asset_discovery/<string:_company_name_>', '/api/metron_data/asset_discovery/<string:_company_name_>/<string:_sites_>')
#api.add_resource(threat_intel, '/api/metron_data/threat_intel', '/api/metron_data/threat_intel/<string:_company_name_>', '/api/metron_data/threat_intel/<string:_company_name_>/<string:_sites_>')
                 
if __name__ == '__main__':
    run_simple('127.0.0.1', 6668, app, use_reloader=True, use_debugger=False, use_evalex=True)
