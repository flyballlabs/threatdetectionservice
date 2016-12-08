#!/usr/bin/python3.5

'''
@summary: Bootstrapper file to run rest_server, and flask api's associated with it.
Ensures all submodules are added to sys path and configures all runtime settings.
@author devopsec
'''
import os
from datetime import datetime
from api import app;
from flask import Flask, make_response, jsonify, g, url_for ,abort, request
from flask_restful import Api  #, marshal, Resource, reqparse, fields
from werkzeug.serving import run_simple
from flask_cors import CORS, cross_origin
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

from api.database import *
from api.sql.models import *

# import endpoints #
from api.auth.endpoint import userAuth
from api.user.endpoint import manageUsers
from api.agent.endpoint import manageAgents, piController
from api.company.endpoint import manageCompany, companyList
#from api.notification.endpoint import manageNotifications
from api.asset.endpoint import manageAssets
from api.metron.endpoint import metronThreats
#from api.metron_data.endpoint import asset_discovery, threat_intel

# flask / sql / api config  #
app = Flask('rest_server')
#app.config['DEBUG'] = False
api = Api(app)
CORS(app)
auth = HTTPBasicAuth()



#for login page, USER is session object for auth user
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    USER = user_data.verify_auth_token(username_or_token)
    if not USER:
        # try to authenticate with username/password
        USER = user_data.query.filter_by(username=username_or_token).first()
        if not USER or not user_data.verify_password(password):
            return False
    g.user_data = USER
    return True

#redir at here to get a token#
@app.route('/api/auth/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

#verify to protect resources
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
        
        
@app.route('/api/users/<int:id>')
def get_userID(id):
    USER = user_data.query.get(id)
    if not USER:
        abort(400)
    return jsonify({'username': USER.username})



'''# hashing functions #
@auth.hash_password
def hash_pw(password):
    return md5(password).hexdigest()

@auth.hash_password
def hash_pw(username, password):
    get_salt(username)
    return hash(password, salt)

@auth.verify_password
def verify_pw(username, password):
    return call_custom_verify_function(username, password)'''


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



api.add_resource(metronThreats, '/api/metron/threats/<string:_device_>')
api.add_resource(manageAssets, '/api/assets/<string:_device_>')

api.add_resource(manageAgents, '/api/agent', '/api/agent/<string:_mac_address_>')
api.add_resource(piController, '/api/picontroller', '/api/picontroller/<string:_mac_address_>')
api.add_resource(userAuth, '/api/auth/<string:_username>/<string:_password>')
api.add_resource(manageUsers, '/api/user', '/api/user/<string:_username_>')
api.add_resource(manageCompany, '/api/company/<string:_company_name_>')
api.add_resource(companyList, '/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites')
#api.add_resource(manageNotifications, '/api/notification', '/api/notification/<string:_username_>')
api.add_resource(manageAssets, '/api/metron_data/asset_discovery/<string:_company_name_>', '/api/metron_data/asset_discovery/<string:_company_name_>/<string:_sites_>', '/api/metron_data/asset_discovery/<string:_company_name_>/<string:_sites_>/<string:_mac_address_>')
#api.add_resource(threat_intel, '/api/metron_data/threat_intel', '/api/metron_data/threat_intel/<string:_company_name_>', '/api/metron_data/threat_intel/<string:_company_name_>/<string:_sites_>')
                 
if __name__ == '__main__':
    if not os.path.exists('db.mysql'):
        db = connect()
        db.create_all()
    app.run(host='0.0.0.0', port=7777, debug=True)
