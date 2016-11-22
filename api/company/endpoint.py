from flask import jsonify
from flask_restful import Resource, reqparse
from sql.models import *  #import all of the models from models.py
from app.parse_json import * #for json request parsing

class manageCompany(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Company name for account', location='json')
            parser.add_argument('address', type=str, help='Address for account', location='json')
            parser.add_argument('city', type=str, help='City location for account', location='json')
            parser.add_argument('state', type=str, help='State location for account', location='json')
            parser.add_argument('zip', type=str, help='Zip code for account', location='json')
            parser.add_argument('phone_number', type=str, help='Company_id for account', location='json')
            parser.add_argument('authinfo', type=json_decode, help='Authentication settings for account', location='json')
            parser.add_argument('sites', type=json_decode, help='List of divisions for account', location='json')
            args = parser.parse_args()#strict=True

            _company_id = args['company_id']
            _company_name = args['company_name']
            _address = args['address']
            _city = args['city']
            _state = args['state']
            _zip = args['zip']
            _phone_number = args['phone_number']
            _authinfo = args['authinfo']
            _sites = args['sites']
            
            query = company_data(company_id=_company_id, company_name=_company_name, address=_address, 
                              city=_city, state=_state, zip=_zip, 
                              phone_number=_phone_number, authinfo=json_encode(_authinfo), sites=json_encode(_sites))

            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                            'status': 200,
                            'message':'Company creation successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status': 400,
                            'message':'Company creation failure'
                        }
        except Exception as e:
            return {'error': str(e)}

    def patch(self, _company_name_):
        try:
            parser = reqparse.RequestParser()
            
            # conditionally replace user data if arg exists #
            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Name of company for account', location='json')
            parser.add_argument('address', type=str, help='Address for account', location='json')
            parser.add_argument('city', type=str, help='City location for account', location='json')
            parser.add_argument('state', type=str, help='State location for account', location='json')
            parser.add_argument('zip', type=str, help='Zip code for account', location='json')
            parser.add_argument('phone_number', type=str, help='Phone_number for account', location='json')
            parser.add_argument('authinfo', type=json_decode, help='Authentication info for account', location='json')
            parser.add_argument('sites', type=json_decode, help='List of divisions for account', location='json')
            
            args = parser.parse_args()#strict=True, require=True
            
            #for response in args:         ############################  
            #    if args[response] != None:# optimize in future release
                
            if args['company_id'] != None:
                _company_id = args['company_id']
            if args['company_name'] != None:
                _company_name = args['company_name']
            if args['address'] != None:
                _address = args['address']
            if args['city'] != None:
                _city = args['city']
            if args['state'] != None:
                _state = args['state']
            if args['zip'] != None:
                _zip = args['zip']
            if args['phone_number'] != None:
                _phone_number = args['phone_number']
            if args['authinfo'] != None:
                _authinfo = args['authinfo']
            if args['sites'] != None:
                _sites = args['sites']
            ###################################
            # would be faster in an array / loop
            
            try:
                curr_session = db.session #open database session
                x = company_data.query.filter_by(company_name=_company_name_).first() #fetch the name to be updated
                x.company_id = _company_id   #update the row
                x.company_name = _company_name
                x.address = _address
                x.city = _city
                x.state = _state
                x.zip = _zip
                x.phone_number = _phone_number
                x.authinfo = json_encode(_authinfo)
                x.sites = json_encode(_sites)
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
        
    def get(self, _company_name_):
        try:
            x = company_data.query.filter_by(company_name=_company_name_).first()
            _company_id = x.company_id
            _company_name = x.company_name
            _address = x.address
            _city = x.city
            _state = x.state
            _zip = x.zip
            _phone_number = x.phone_number
            _authinfo = x.authinfo #json_decode()
            _sites = x.sites
            
            if x != None:
                return {
                        'company_id':_company_id,
                        'company_name':_company_name,
                        'address' : _address,
                        'city' : _city,
                        'zip' : _zip,
                        'phone_number' : _phone_number,
                        'authinfo' : _authinfo, #json_encode() / jsonify()
                        'sites' : _sites,
                        'message':'User search success'
                       }
            else:
                return {
                        'status': 400,
                        'message':'User search failure'
                       }
        except Exception as e:
            return {'error': str(e)}
        
    def delete(self, _company_name_):
        try:
            curr_session = db.session #open database session
            x = company_data.query.filter_by(company_name=_company_name_).first()
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
