from flask_restful import Resource, reqparse
from sql.models import *  #import all of the models from models.py
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

    def patch(self, _username_):
        try:
            parser = reqparse.RequestParser()
            
            # conditionally replace user data if arg exists #
            parser.add_argument('user_id', type=int, help='Username for account', location='json')
            # You can't change your username once it's selected
	    #parser.add_argument('username', type=str, help='Password for account', location='json')
            parser.add_argument('firstname', type=str, help='Firstname for account', location='json')
            parser.add_argument('lastname', type=str, help='Lastname for account', location='json')
            parser.add_argument('password', type=str, help='Password for account', location='json')
            parser.add_argument('email', type=str, help='Email for account', location='json')
            parser.add_argument('company_id', type=str, help='Company_id for account', location='json')
            parser.add_argument('status', type=str, help='Status for account', location='json')
            parser.add_argument('lastlogin', type=str, help='Lastlogin for account', location='json')
            
            args = parser.parse_args()#strict=True, require=True
            
            #for response in args:         ############################  
            #    if args[response] != None:# optimize in future release
            try:
 
                curr_session = db.session
                x = user_data.query.filter_by(username=_username_).first()
 
                if args['user_id'] != None:
                   x.user_id = args['user_id']
                if args['firstname'] != None:
                   x.firstname = args['firstname']
                if args['lastname'] != None:
                   x.lastname = args['lastname']
                if args['password'] != None:
                   x.password = args['password']
                if args['email'] != None:
                   x.email = args['email']
                if args['company_id'] != None:
                   x.company_id = args['company_id']
                if args['status'] != None:
                   x.status = args['status']
                if args['lastlogin'] != None:
                   x.lastlogin = args['lastlogin']
            
                print(args['lastname'])
                curr_session.commit()  #commit changes
                
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
            _lastlogin = x.lastlogin
            
            if x != None:
                return {
                        'user_id':_user_id,
                        'username':_username_,
                        'firstname' : _firstname,
                        'lastname' : _lastname,
                        'email' : _email,
                        'company_id' : _company_id,
                        'status' : _status,
                        'lastlogin' : _lastlogin,
                        'message':'User search success'
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
