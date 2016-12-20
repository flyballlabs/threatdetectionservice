from flask import jsonify, request
from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
from api.app.parse_json import * #for json arg parsing

class manageCompany(Resource):
    # update a company's info #
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
            parser.add_argument('poc', type=str, help='Point Of Contact for account', location='json')
            parser.add_argument('authinfo', type=str, help='Authentication info for account', location='json')
            parser.add_argument('sites', type=str, help='List of divisions for account', location='json')
            
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
            if args['poc'] != None:
                _poc = args['poc']
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
                x.poc = _poc
                x.authinfo = _authinfo #json_encode()
                x.sites = _sites
                curr_session.commit() #commit changes
                
                return  {
                            'status': 200,
                            'message':'Company update successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status':400,
                            'message':'Company update failure'
                        }
        except Exception as e:
            return {'error': str(e)}
        
    # get info about a company #
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
            _poc = x.poc
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
                        'poc' : _poc,
                        'authinfo' : _authinfo, #json_encode() / jsonify()
                        'sites' : _sites
                       }
            else:
                return {
                        'status': 400,
                        'message':'User search failure'
                       }
        except Exception as e:
            return {'error': str(e)}
        
    # delete a company #
    def delete(self, _company_name_):
        try:
            curr_session = db.session #open database session
            x = company_data.query.filter_by(company_name=_company_name_).first()
            try:
                db.session.delete(x)
                db.session.commit()
                return  {
                            'status': 200,
                            'message':'Company delete successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status':400,
                            'message':'Company delete failure'
                        }
        except Exception as e:
            return {'error': str(e)}
        
        
class companyList(Resource):
    # add to list / create new company #
    def post(self):
        try:
            args = request.get_json(force=True)
            
            parser = reqparse.RequestParser()
            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Company name for account', location='json')
            parser.add_argument('address', type=str, help='Address for account', location='json')
            parser.add_argument('city', type=str, help='City location for account', location='json')
            parser.add_argument('state', type=str, help='State location for account', location='json')
            parser.add_argument('zip', type=str, help='Zip code for account', location='json')
            parser.add_argument('phone_number', type=str, help='Company_id for account', location='json')
            parser.add_argument('poc', type=str, help='Point Of Contact for account', location='json')
            parser.add_argument('authinfo', type=list, help='Authentication settings for account', location='json')
            parser.add_argument('sites', type=list, help='List of divisions for account', location='json')
            args = parser.parse_args()#strict=True
            #return jsonify(args)
            #temp1 = json_decode(args['authinfo'])
            #temp2 = json_encode(args['sites'])
            
            _company_id = args['company_id']
            _company_name = args['company_name']
            _address = args['address']
            _city = args['city']
            _state = args['state']
            _zip = args['zip']
            _phone_number = args['phone_number']
            _poc = args['poc']
            _authinfo = args['authinfo']
            _sites = args['sites']
            
            #query = jsonify(args.authinfo) jsonify(args.sites)
            query = company_data(company_id=_company_id, company_name=_company_name, address=_address, 
                              city=_city, state=_state, zip=_zip, phone_number=_phone_number, 
                              poc=_poc, authinfo=_authinfo, sites=_sites)
            return query
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
    
    # _company_name_ is optional param #
    def get(self, _company_name_=None):
        URL = request.url
        # get a list of sites for specified company #
        if URL.find("api/company") > 0 and URL.find("sites") > 0 and _company_name_ != None:
            try: 
                x = company_data.query.filter_by(company_name=_company_name_).first()
                if x != None:
                    return jsonify(sites=x.sites)
                else:
                    return {
                            'status': 400,
                            'message':'Company sites for specified company are not available'
                           }
            except Exception as e:
                return {'error': str(e)}
            
        # get list of all sites #
        elif URL.find("api/company/sites") > 0 and _company_name_ == None:
            try: # .load_only("company_name")
                x = company_data.query.with_entities(company_data.sites).all()
               
                if x != None:
                    return jsonify(companies=x)
                else:
                    return {
                            'status': 400,
                            'message':'Company sites are not available'
                           }
            except Exception as e:
                return {'error': str(e)}
            
        # get a list of all companies #
        elif URL.find("api/company") > 0 and _company_name_ == None:
            try: 
                x = company_data.query.with_entities(company_data.company_name).all()
               
                if x != None:
                    return jsonify(x)
                else:
                    return {
                            'status': 400,
                            'message': 'Company names are not available'
                           }
            except Exception as e:
                return {'error': str(e)}
            
        else:
            return {
                    'status': 404,
                    'message':'Redirection error, route is not available'
                   }
            