#!/usr/bin/python3.5

'''
@summary: Bootstrapper file to run rest_server, and flask api's associated with it.
Ensures all submodules are added to sys path and configures all runtime settings.
@author devopsec
'''

from app import *
from flask import Flask, make_response, jsonify #, request, abort, render_template, Flask
from flask_restful import Api, reqparse, fields #, marshal, Resource
from flask_cors import CORS, cross_origin
#from flask.ext.security import current_user, login_required, RoleMixin, Security, \
#    SQLAlchemyUserDatastore, UserMixin, utils

# import endpoints #
from auth.endpoint import *
from user.endpoint import *
from agent.endpoint import *
from company.endpoint import *
from metron.endpoint import *
from asset.endpoint import *

# import models
from sql.models import *

# flask / sql / api config  #
app = Flask('rest_server')
app.config['DEBUG'] = True
# SECRET_KEY is used by Flask to encrypt data in the Session object
app.config['SECRET_KEY'] = 'flyball2016'
api = Api(app)
CORS(app)

# Secret configuration for Flask-Security
# Specify the security has PBKDF2 with salt.
#app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
# Replace this with your own salt.
#app.config['SECURITY_PASSWORD_SALT'] = 'flyball2016' 

# Create a table to support a many-to-many relationship between Users and Roles
#roles_users = db.Table(
#    'roles_users',
#    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
#)



@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

api.add_resource(manageAgent, '/api/agent/<string:_mac_address_>')
api.add_resource(manageAgentList, '/api/agent')
#api.add_resource(timeSync, '/api/picontroller/time')
#api.add_resource(piController, '/api/picontroller/<string:id>')
#api.add_resource(update, '/api/picontroller/<string:id>/<string:start>/<string:end>/<string:cmd>')
api.add_resource(userAuth, '/api/auth/<string:_username>/<string:_password>')

api.add_resource(manageUser, '/api/user/<string:_username_>')
api.add_resource(manageUserList, '/api/user')

api.add_resource(manageCompany, '/api/company/<string:_company_name_>')
api.add_resource(manageCompanyList, '/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites')

api.add_resource(metronThreats, '/api/metron/threats/<string:_device_>')
api.add_resource(manageAssets, '/api/assets/<string:_device_>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=False)
