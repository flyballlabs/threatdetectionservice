'''from flask import jsonify, request
from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
from api.app.parse_json import * #for json arg parsing


class manageNotifications(object):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int, help='User_id for account', location='json')
            parser.add_argument('username', type=str, help='Username for account', location='json')
            parser.add_argument('firstname', type=str, help='Firstname for account', location='json')
            parser.add_argument('lastname', type=str, help='Lastname for account', location='json')
            parser.add_argument('password', type=str, help='Password for account', location='json')
            parser.add_argument('email', type=str, help='Email for account', location='json')
            parser.add_argument('company_id', type=str, help='Company_id for account', location='json')
            parser.add_argument('status', type=str, help='Status for account', location='json')
            parser.add_argument('lastlogin', type=str, help='Lastlogin for account', location='json')
            args = parser.parse_args()#strict=True

            _user_id = args['user_id']
            _username = args['username']
            _firstname = args['firstname']
            _lastname = args['lastname']
            _password = args['password']
            _email = args['email']
            _company_id = args['company_id']
            _status = args['status']
            _lastlogin = args['lastlogin']
            
            query = user_data(user_id=_user_id, username=_username, firstname=_firstname, 
                              lastname=_lastname, password=_password, email=_email, 
                              company_id=_company_id, status=_status, lastlogin=_lastlogin)

            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                            'status': 200,
                            'message':'User creation successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status': 400,
                            'message':'User creation failure'
                        }
        except Exception as e:
            return {'error': str(e)}
'''