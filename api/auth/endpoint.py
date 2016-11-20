from flask_restful import Resource, reqparse
from sql.models import *  #import all of the models from models.py


class userAuth(Resource):
    def get(self,username,password):
        try:
            #parser = reqparse.RequestParser()
            #parser.add_argument('username', type=str, help='Username for account')
            #parser.add_argument('password', type=str, help='Password for account')
            #args = parser.parse_args()

            #_username = args['username']
            #_password = args['password']

            _username = username
            _password = password
        
            x = user_data.query.filter_by(username=_username).first()
            if x != None:
                if x.password == _password:
                    return {
                            'authentication': True,
                            'message':'Authentication success'
                           }
                else:
                    return {
                            'authentication': False,
                            'message':'Authentication failure'
                           }
        except Exception as e:
            return {'error': str(e)}
