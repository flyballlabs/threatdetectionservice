#!/usr/bin/python3.5

'''
@summary: Bootstrapper file to run rest_server, and flask api's associated with it.
Ensures all submodules are added to sys path and configures all runtime settings.
@author devopsec
'''

from app import *
from flask import Flask, make_response, jsonify #, request, abort, render_template, Flask
from flask_restful import Api, reqparse, fields #, marshal, Resource

# import endpoints #
from auth.endpoint import *
from user.endpoint import *
from agent.endpoint import *
from company.endpoint import *


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
#api.add_resource(timeSync, '/api/picontroller/time')
#api.add_resource(piController, '/api/picontroller/<string:id>')
#api.add_resource(update, '/api/picontroller/<string:id>/<string:start>/<string:end>/<string:cmd>')
api.add_resource(userAuth, '/api/auth/<string:_username>/<string:_password>')
api.add_resource(manageUsers, '/api/user', '/api/user/<string:_username_>')
api.add_resource(manageCompany, '/api/company/<string:_company_name_>')
api.add_resource(companyList, '/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6668, debug=False)
