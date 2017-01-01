from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
#from flask_login import login_user , logout_user , current_user , login_required
from api import *

class userAuth(Resource):
    def get(self,_username,_password):
        try:
            #parser = reqparse.RequestParser()
            #parser.add_argument('username', type=str, help='Username for account')
            #parser.add_argument('password', type=str, help='Password for account')
            #args = parser.parse_args()
            
            #_username = args['username']
            #_password = args['password']

            #_username = username
            #_password = password
        
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
