from flask import jsonify
from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
from api import *

class userAuth(Resource):
    def get(self,_username,_password):
        try:            
            x = user_data.query.filter_by(username=_username).first()
            if x != None:
                if x.password == _password:
                   login_user(x)
                   retMessage = {}
                   retMessage['authentication'] = True
                   retMessage['message'] = 'Authentication success'
                   retMessage['X-AUTH-TOKEN'] = x.generate_auth_token().decode('ascii')
                   return jsonify(**retMessage)
                else:
                    return {
                            'authentication': False,
                            'message':'Authentication failure'
                           }
            else:
                return {
                        'status': 400,
                        'message':'User search failure'
                       }
        except Exception as e:
            return {'error': str(e)}

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
                   return jsonify(**retMessage)
            else:
                return {
                        'status': 400,
                        'message':'User search failure'
                       }
        except Exception as e:
            return {'error': str(e)}
