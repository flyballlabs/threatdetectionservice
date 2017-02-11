from api import *
from api import db, user_data
from flask_login import login_required
from flask_restful import reqparse

class manageUser(Resource):
    @login_required
    def get(self, _username_):
        try:
            x = user_data.query.filter_by(username=_username_).first()
            _user_id = x.user_id
            _firstname = x.firstname
            _lastname = x.lastname
            _email = x.email
            _company_id = x.company_id
            _active = x.active
            _phone_number = x.phone_number
            _lastlogin = x.lastlogin
            _account_type = x.account_type
            _notification = x.notification
            
            if x != None:
                return {
                    'status' : 200,
                    'message' : 'User search success',
                    'user_id' : _user_id,
                    'username' : _username_,
                    'firstname' : _firstname,
                    'lastname' : _lastname,
                    'email' : _email,
                    'company_id' : _company_id,
                    'active' : _active,
                    'phone_number' : _phone_number,
                    'lastlogin' : _lastlogin,
                    'account_type' : _account_type,
                    'notification' : _notification
                }
            else:
                return {
                    'status' : 400,
                    'message' :'User search failure'
                }
        except Exception as e:
            return {'error' : str(e)} # DEBUG only (security risk : TMI)
    
    @login_required    
    def put(self, _username_):
        try:
            parser = reqparse.RequestParser()
            
            # conditionally replace user data if arg exists #
            parser.add_argument('user_id', type=int, help='Username for account', location='json')
            parser.add_argument('username', type=str, help='Password for account', location='json')
            parser.add_argument('firstname', type=str, help='Firstname for account', location='json')
            parser.add_argument('lastname', type=str, help='Lastname for account', location='json')
            parser.add_argument('password', type=str, help='Password for account', location='json')
            parser.add_argument('email', type=str, help='Email for account', location='json')
            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('active', type=TINYINT, help='Is account active', location='json')
            parser.add_argument('phone_number', type=str, help='Phone Number for account', location='json')
            parser.add_argument('lastlogin', type=str, help='Lastlogin for account', location='json')
            parser.add_argument('account_type', type=str, help='Account priveledge level', location='json')
            parser.add_argument('notification', type=json_encode, help='Notification settings', location='json')
            
            args = parser.parse_args() #strict=True, require=True
            curr_session = db.session  # open database session

            try:
                x = user_data.query.filter_by(username=_username_).first() #fetch the username to be updated
                if args['user_id'] != None:
                    x.user_id = args['user_id']                
                if args['username'] != None:
                    x.username = args['username']
                if args['firstname'] != None:
                    x.firstname = args['firstname']
                if args['lastname'] != None:
                    x.lastname = args['lastname']		
                if args['password'] != None:
                    x._password = args['password']
                if args['email'] != None:
                    x.email = args['email']
                if args['company_id'] != None:
                    x.company_id = args['company_id']
                if args['active'] != None:
                    x.active = args['active']
                if args['phone_number'] != None:
                    x.phone_number = args['phone_number']
                if args['lastlogin'] != None:
                    x.lastlogin = args['lastlogin']
                if args['account_type'] != None:
                    x.account_type = args['account_type']
                if args['notification'] != None:
                    x.notification = json_decode(args['notification'])

                curr_session.commit() #commit changes
                
                return {
                    'status' : 200,
                    'message' :'User update successful'
                }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return {
                    'status' : 400,
                    'message' : 'User update failure'
                }
        except Exception as e:
            return {'error' : str(e)} # DEBUG only (security risk : TMI)
        
    @login_required    
    def delete(self, _username_):
        try:
            curr_session = db.session #open database session
            x = user_data.query.filter_by(username=_username_).first()
            try:
                db.session.delete(x)
                db.session.commit()
                return {
                    'status' : 200,
                    'message' : 'User delete successful'
                }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return {
                    'status' : 400,
                    'message' : 'User delete failure'
                }
        except Exception as e:
            return {'error' : str(e)} # DEBUG only (security risk : TMI)

class manageUserList(Resource):
    @login_required    
    def get(self):
        try:
            x = user_data.query.all()
            if x != None:
                results = []
                for user in x:
                    results.append( {
                        'user_id' : user.user_id,
                        'username' : user.username,
                        'firstname' : user.firstname,
                        'lastname' : user.lastname,
                        'email' : user.email,
                        'company_id' : user.company_id,
                        'active' : user.active,
                        'phone_number' : user.phone_number,
                        'lastlogin' : user.lastlogin,
                        'account_type' : user.account_type,
                        'notification' : user.notification
                    } )

                return jsonify(
                    status = 200,
                    message = 'User search success',
                    users = results
                )
            else:
                return {
                    'status' : 400,
                    'message' : 'User search failure'
                }
        except Exception as e:
            return {'error' : str(e)} # DEBUG only (security risk : TMI)
    
    @login_required    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=int, help='User_id for account', location='json')
            parser.add_argument('username', type=str, help='Username for account', location='json')
            parser.add_argument('firstname', type=str, help='Firstname for account', location='json')
            parser.add_argument('lastname', type=str, help='Lastname for account', location='json')
            parser.add_argument('password', type=str, help='Password for account', location='json')
            parser.add_argument('email', type=str, help='Email for account', location='json')
            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('active', type=TINYINT, help='Status for account', location='json')
            parser.add_argument('phone_number', type=str, help='Phone Number for account', location='json')
            parser.add_argument('lastlogin', type=str, help='Lastlogin for account', location='json')
            parser.add_argument('account_type', type=str, help='Account priveledge level', location='json')
            parser.add_argument('notification', type=json_encode, help='Notification settings', location='json')
            args = parser.parse_args()#strict=True

            _user_id = args['user_id']
            _username = args['username']
            _firstname = args['firstname']
            _lastname = args['lastname']
            _password = args['password']
            _email = args['email']
            _company_id = args['company_id']
            _active = args['active']
            _phone_number = args['phone_number']
            _lastlogin = args['lastlogin']
            _account_type = args['account_type']
            _notification = args['notification']
            
            query = user_data(user_id=_user_id, username=_username, firstname=_firstname, lastname=_lastname,
                              password=_password, email=_email, company_id=_company_id, active=_active,
                              phone_number=_phone_number, lastlogin=_lastlogin, account_type=_account_type,
                              notification=json_decode(_notification))

            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                    'status' : 200,
                    'message' : 'User creation successful'
                }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                    'status' : 400,
                    'message' : 'User creation failure'
                }
        except Exception as e:
            return {'error': str(e)} # DEBUG only (security risk : TMI)
