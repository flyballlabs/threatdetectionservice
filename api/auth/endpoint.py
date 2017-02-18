'''
@Summary: Authenticates users through password or token authentication.
Authenticated users are then logged into a session using flask_login.
'''

from flask import jsonify
from flask_login import login_user
from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py

class userAuth(Resource):
    def get(self, _username, _password):
        try:            
            x = user_data.query.filter_by(username=_username).first()
            if x != None:
                if x.password == _password:
                    login_user(x)
                    retMessage = {}
                    retMessage['authentication'] = True
                    retMessage['message'] = 'Authentication success'
                    retMessage['X-AUTH-TOKEN'] = x.generate_auth_token().decode('ascii')
                    return jsonify(
                        status = 200,
                        **retMessage
                    )
                else:
                    return {
                        'status': 401,
                        'authentication': False,
                        'message': 'Authentication failure'
                   }
            else:
                return {
                    'status': 400,
                    'message': 'User search failure'
               }
        except Exception as e:
            return {'status': 400}

# TODO: we aren't using this? determine seperation of duties for auth
class userAuthToken(Resource):
    def get(self):
        try:
            _username="mack@goflyball.com"           
            x = user_data.query.filter_by(username=_username).first()
            if x != None:
                retMessage = {}
                retMessage['authentication'] = True
                retMessage['message'] = 'Authentication success'
                retMessage['X-AUTH-TOKEN'] = x.generate_auth_token().decode('ascii')
                return jsonify(
                    status = 200,
                    **retMessage
                )
            else:
                return {
                    'status': 400,
                    'message':'User search failure'
                }
        except Exception as e:
            return {'status': 400}
