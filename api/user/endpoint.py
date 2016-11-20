from flask_restful import Resource, reqparse
from sql import models

class manageUsers(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, help='Username for account', strict=True)
            parser.add_argument('username', type=str, help='Password for account', strict=True)
            parser.add_argument('firstname', type=str, help='Username for account', strict=True)
            parser.add_argument('lastname', type=str, help='Username for account', strict=True)
            parser.add_argument('password', type=str, help='Username for account', strict=True)
            parser.add_argument('email', type=str, help='Username for account', strict=True)
            parser.add_argument('company_id', type=str, help='Username for account', strict=True)
            parser.add_argument('status', type=str, help='Username for account', strict=True)
            parser.add_argument('lastlogin', type=str, help='Username for account', strict=True)
            args = parser.parse_args()

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

    def patch(self):
        try:
            parser = reqparse.RequestParser()
            
            # conditionally replace user data if arg exists #
            parser.add_argument('user_id', type=str, help='Username for account', strict=True)
            parser.add_argument('username', type=str, help='Password for account', strict=True, require=True)
            parser.add_argument('firstname', type=str, help='Username for account', strict=True)
            parser.add_argument('lastname', type=str, help='Username for account', strict=True)
            parser.add_argument('password', type=str, help='Username for account', strict=True)
            parser.add_argument('email', type=str, help='Username for account', strict=True)
            parser.add_argument('company_id', type=str, help='Username for account', strict=True)
            parser.add_argument('status', type=str, help='Username for account', strict=True)
            parser.add_argument('lastlogin', type=str, help='Username for account', strict=True)
            args = parser.parse_args()
            _username = args['username']
            
            if args['user_id'] != None:
                _user_id = args['user_id']
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
            if args['lastlogin'] != None:
                _lastlogin = args['lastlogin']
            
            ###################################
            # add args to an array as tuples indicating if it should be updated (if arg was not None)
            
            try:
                x = user_data.query.filter_by(username=_username).first() #fetch the username do be updated
                
                ###################################
                # for loop updating the the column values from the array

#                 with x:     #update the column
#                     .username = _username
#                     .firstname = _firstname
#                     .lastname = _lastname
                curr_session.commit() #commit changes
                return  {
                            'status': 200,
                            'message':'User update successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status': 400,
                            'message':'User update failure'
                        }
        except Exception as e:
            return {'error': str(e)}
        
    def get(self, username):
        try:
            x = user_data.query.filter_by(username=username).first()
            _user_id = x.user_id
            _firstname = x.firstname
            _lastname = x.lastname
            _email = x.email
            _company_id = x.company_id
            _status = x.status
            _lastlogin = x.lastlogin
            
            if x != None:
                if x.password == _password:
                    return {
                            'firstname' : _firstname,
                            'lastname' : _lastname,
                            'email' : _email,
                            'company_id' : _company_id,
                            'status' : _status,
                            'lastlogin' : _lastlogin,
                            'user_id': _user_id,
                            'message':'User search success'
                           }
                else:
                    return {
                            'status': 200,
                            'message':'User search failure'
                           }
        except Exception as e:
            return {'error': str(e)}      
