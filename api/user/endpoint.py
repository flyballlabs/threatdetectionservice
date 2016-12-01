from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
#from app.parse_json import * #for json request parsing

class manageUsers(Resource):
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
            parser.add_argument('phone_number', type=str, help='Phone Number for account', location='json')
            parser.add_argument('lastlogin', type=str, help='Lastlogin for account', location='json')
            parser.add_argument('ph', type=str, help='Priveledge level for account', location='json')
            parser.add_argument('notification', type=str, help='Notification settings for account', location='json')
            args = parser.parse_args()#strict=True

            _user_id = args['user_id']
            _username = args['username']
            _firstname = args['firstname']
            _lastname = args['lastname']
            _password = args['password']
            _email = args['email']
            _company_id = args['company_id']
            _status = args['status']
            _phone_number = args['phone_number']
            _lastlogin = args['lastlogin']
            _account_type = args['account_type']
            _notification = args['notification']
            
            query = user_data(user_id=_user_id, username=_username, firstname=_firstname, 
                              lastname=_lastname, password=_password, email=_email, 
                              company_id=_company_id, status=_status, phone_number=_phone_number,
                              lastlogin=_lastlogin, account_type=_account_type, notification=_notification)

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

    def patch(self, _username_):
        try:
            parser = reqparse.RequestParser()
            
            # conditionally replace user data if arg exists #
            parser.add_argument('user_id', type=int, help='Username for account', location='json')
            parser.add_argument('username', type=str, help='Password for account', location='json')
            parser.add_argument('firstname', type=str, help='Firstname for account', location='json')
            parser.add_argument('lastname', type=str, help='Lastname for account', location='json')
            parser.add_argument('password', type=str, help='Password for account', location='json')
            parser.add_argument('email', type=str, help='Email for account', location='json')
            parser.add_argument('company_id', type=str, help='Company_id for account', location='json')
            parser.add_argument('status', type=str, help='Status for account', location='json')
            parser.add_argument('phone_number', type=str, help='Phone Number for account', location='json')
            parser.add_argument('lastlogin', type=str, help='Lastlogin for account', location='json')
            parser.add_argument('account_type', type=str, help='Priveledge level for account', location='json')
            parser.add_argument('notification', type=str, help='Notification settings for account', location='json')
            
            args = parser.parse_args()#strict=True, require=True
            
            #for response in args:         ############################  
            #    if args[response] != None:# optimize in future release
                
            if args['user_id'] != None:
                _user_id = args['user_id']
            if args['username'] != None:
                _username = args['username']
            if args['firstname'] != None:
                _firstname = args['firstname']
            if args['lastname'] != None:
                _lastname = args['lastname']
            if args['password'] != None:
                _password = args['password']
            if args['email'] != None:
                _email = args['email']
            if args['company_id'] != None:
                _company_id = args['company_id']
            if args['status'] != None:
                _status = args['status']
            if args['phone_number'] != None:
                _phone_number = args['phone_number']
            if args['lastlogin'] != None:
                _lastlogin = args['lastlogin']
            if args['account_type'] != None:
                _account_type = args['account_type']
            if args['notification'] != None:
                _notification = args['notification']
            ###################################
            # would be faster in an array / loop
            
            try:
                curr_session = db.session #open database session
                x = user_data.query.filter_by(username=_username_).first() #fetch the username to be updated
                x.user_id = _user_id   #update the row
                x.username = _username
                x.firstname = _firstname
                x.lastname = _lastname
                x.password = _password
                x.email = _email
                x.company_id = _company_id
                x.status = _status
                x.phone_number = _phone_number
                x.lastlogin = _lastlogin
                x.account_type = _account_type
                x.notification = _notification
                curr_session.commit() #commit changes
                
                return  {
                            'status': 200,
                            'message':'User update successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status':400,
                            'message':'User update failure'
                        }
        except Exception as e:
            return {'error': str(e)}
        
    
    def get(self, _username_):
        try:
            x = user_data.query.filter_by(username=_username_).first()
            _user_id = x.user_id
            _firstname = x.firstname
            _lastname = x.lastname
            _email = x.email
            _company_id = x.company_id
            _status = x.status
            _phone_number = x.phone_number
            _lastlogin = x.lastlogin
            _account_type = x.account_type
            _notification = x.notification
            
            if x != None:
                return {
                        'user_id':_user_id,
                        'username':_username_,
                        'firstname' : _firstname,
                        'lastname' : _lastname,
                        'email' : _email,
                        'company_id' : _company_id,
                        'status' : _status,
                        'phone_number' : _phone_number,
                        'lastlogin' : _lastlogin,
                        'account_type' : _account_type,
                        'notification' : _notification
                       }
            else:
                return {
                        'status': 400,
                        'message':'User search failure'
                       }
        except Exception as e:
            return {'error': str(e)}
        
    def delete(self, _username_):
        try:
            curr_session = db.session #open database session
            x = user_data.query.filter_by(username=_username_).first()
            try:
                db.session.delete(x)
                db.session.commit()
                return  {
                            'status': 200,
                            'message':'User delete successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status':400,
                            'message':'User delete failure'
                        }
        except Exception as e:
            return {'error': str(e)}
