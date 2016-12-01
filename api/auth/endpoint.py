from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py

class userAuth(Resource):
    def get(self, _username, _password):
        try:
            x = user_data.query.all()
            table = user_table(x) # Populate the table
            print(table.__html__())
            
            x = user_data.query.filter_by(username=_username).first()
            if x != None:
                if x.password == _password:
                    curr_session = db.session
                    if x.account_type == 'user':
                        x.status = 1
                    elif x.account_type == 'admin':
                        x.status = 2
                    elif x.account_type == 'su':
                        x.status = 3
                    curr_session.commit() #commit changes
                    return {
                            'authentication': True,
                            #auth level: 1 - user, 2 - admin, 3 su
                            'account_type': x.account_type 
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
            curr_session.rollback()
            curr_session.flush()
            return {'error': str(e)}
