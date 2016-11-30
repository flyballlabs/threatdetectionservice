from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py

class userAuth(Resource):
    def get(self, _username, _password):
        try:
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
            else:
                return {
                        'status': 400,
                        'message':'User search failure'
                       }
        except Exception as e:
            return {'error': str(e)}
