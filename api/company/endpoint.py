from flask import jsonify, request
from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
from api.util.parse_json import json_decode, json_encode #for json request parsing
from api import login_required, db


class companyUtils:
    ''' Decoupling of re-usable methods in a static context
        Note: jsonify does not handle lists and isn't used here '''

    @staticmethod
    def get_company_poc_list(_company_name_):
        try:
            x = company_data.query.filter_by(company_name=_company_name_).first()
            if x != None:
                return {
                    'status' : 200,
                    'poc' : x.poc
                }
            else:
                return {
                    'status' : 400,
                    'message' : 'Company POCs for specified company are not available'
                }
        except Exception as e:
            return {'status' : 400}

    @staticmethod
    def get_all_poc_list():
        try: # load_only("company_name")
            x = company_data.query.all()
            if x != None:
                co_poc_list = []
                for co in x:
                    co_poc_list.append({
                        'company_name' : co.company_name,
                        'poc' : co.poc
                    })

                return {
                    'status' : 200,
                    'all_company_poc' : co_poc_list
                }
            else:
                return {
                    'status' : 400,
                    'message' : 'Company POCs are not available'
                }
        except Exception as e:
            return {'status' : 400}

class manageCompany(Resource):
    @login_required    
    def get(self, _company_name_): # get all info about a company #
        try:
            x = company_data.query.filter_by(company_name=_company_name_).first()
            _company_id = x.company_id
            _company_name = x.company_name
            _street = x.street
            _city = x.city
            _state = x.state
            _zip = x.zip
            _phone_number = x.phone_number
            _poc = x.poc
            _authinfo = x.authinfo
            _sites = x.sites

            if x != None:
                return jsonify(
                    status = 200,
                    message = 'Company search success',
                    company_id = _company_id,
                    company_name = _company_name,
                    street = _street,
                    city = _city,
                    state = _state,
                    zip = _zip,
                    phone_number = _phone_number,
                    poc = _poc,
                    authinfo = _authinfo,
                    sites = _sites
                )
            else:
                return {
                    'status' : 400,
                    'message' : 'Company search failure'
                }
        except Exception as e:
            return {'status' : 400}
    
    @login_required    
    def put(self, _company_name_): # update a company's info #
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Name of company for account', location='json')
            parser.add_argument('street', type=str, help='street for account', location='json')
            parser.add_argument('city', type=str, help='City location for account', location='json')
            parser.add_argument('state', type=str, help='State location for account', location='json')
            parser.add_argument('zip', type=str, help='Zip code for account', location='json')
            parser.add_argument('phone_number', type=str, help='Phone_number for account', location='json')
            parser.add_argument('poc', type=json_encode, help='Point Of Contact List for account', location='json')
            parser.add_argument('authinfo', type=json_encode, help='Authentication info for account', location='json')
            parser.add_argument('sites', type=json_encode, help='List of divisions for account', location='json')

            args = parser.parse_args()
            curr_session = db.session  # open database session

            try:
                x = company_data.query.filter_by(company_name=_company_name_).first() #fetch the name to be updated

                if args['company_id'] != None:
                    x.company_id = args['company_id']
                if args['company_name'] != None:
                    x.company_name = args['company_name']
                if args['street'] != None:
                    x.street = args['street']
                if args['city'] != None:
                    x.city = args['city']
                if args['state'] != None:
                    x.state = args['state']
                if args['zip'] != None:
                    x.zip = args['zip']
                if args['phone_number'] != None:
                    x.phone_number = args['phone_number']
                if args['poc'] != None:
                    x.poc = json_decode(args['poc'])
                if args['authinfo'] != None:
                    x.authinfo = json_decode(args['authinfo'])
                if args['sites'] != None:
                    x.sites = json_decode(args['sites'])
                
                curr_session.commit() #commit changes
                
                return {
                    'status' : 200,
                    'message' : 'Company update successful'
                }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return {
                    'status' : 400,
                    'message' : 'Company update failure'
                }
        except Exception as e:
            return {'status' : 400}
        
    @login_required    
    def delete(self, _company_name_): # delete a company #
        try:
            curr_session = db.session #open database session
            x = company_data.query.filter_by(company_name=_company_name_).first()
            try:
                db.session.delete(x)
                db.session.commit()
                return {
                    'status' : 200,
                    'message' : 'Company delete successful'
                }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return {
                    'status' : 400,
                    'message' : 'Company delete failure'
                }
        except Exception as e:
            return {'status' : 400}

class manageCompanyList(Resource):
    '''contains methods for accessing resource lists from company table in mysql'''

    @login_required
    def get(self, _company_name_=None): # _company_name_ is optional param #
        URL = request.url
        # get a list of sites for specified company #
        if URL.find("api/company") > 0 and URL.find("sites") > 0 and _company_name_ != None:
            try: 
                x = company_data.query.filter_by(company_name=_company_name_).first()
                if x != None:
                    return jsonify(
                        status = 200,
                        sites = x.sites
                    )
                else:
                    return {
                        'status' : 400,
                        'message' : 'Company sites for specified company are not available'
                    }
            except Exception as e:
                return {'status' : 400}
            
        # get list of all sites #
        elif URL.find("api/company/sites") > 0 and _company_name_ == None:
            try: # .load_only("company_name")
                x = company_data.query.all()
                if x != None:
                    co_site_dict = {}
                    for co in x:
                        co_site_dict[co.company_name] = co.sites
                    return jsonify(
                        status = 200,
                        company_sites = co_site_dict
                    )
                else:
                    return {
                        'status' : 400,
                        'message' : 'Company sites are not available'
                    }
            except Exception as e:
                return {'status' : 400}

        # get a list of poc's for specified company #
        if URL.find("api/company") > 0 and URL.find("poc") > 0 and _company_name_ != None:
            return companyUtils.get_company_poc_list(_company_name_)
            
        # get list of all poc's for all companies #
        elif URL.find("api/company/poc") > 0 and _company_name_ == None:
            return companyUtils.get_all_poc_list()
            
        # get a list of all companies #
        elif URL.find("api/company") > 0 and _company_name_ == None:
            try: 
                x = company_data.query.with_entities(company_data.company_name).all()
               
                if x != None:
                    companyList = []
                    for co in x:
                        companyList.append(co[0])
                    return jsonify(
                        status = 200,
                        companies = companyList
                    )
                else:
                    return {
                        'status' : 400,
                        'message' : 'Company names are not available'
                   }
            except Exception as e:
                return {'status' : 400}
            
        else:
            return {
                'status' : 404,
                'message' : 'Redirection error, route is not available'
            }

    # add to list / create new company #
    @login_required    
    def post(self):
        try:
            parser = reqparse.RequestParser()

            parser.add_argument('company_id', type=int, help='Company_id for account', location='json')
            parser.add_argument('company_name', type=str, help='Company name for account', location='json')
            parser.add_argument('street', type=str, help='street for account', location='json')
            parser.add_argument('city', type=str, help='City location for account', location='json')
            parser.add_argument('state', type=str, help='State location for account', location='json')
            parser.add_argument('zip', type=str, help='Zip code for account', location='json')
            parser.add_argument('phone_number', type=str, help='Company_id for account', location='json')
            parser.add_argument('poc', type=json_encode, help='Point Of Contact for account', location='json')
            parser.add_argument('authinfo', type=json_encode, help='Authentication settings for account', location='json')
            parser.add_argument('sites', type=json_encode, help='List of divisions for account', location='json')

            args = parser.parse_args()
            
            _company_id = args['company_id']
            _company_name = args['company_name']
            _street = args['street']
            _city = args['city']
            _state = args['state']
            _zip = args['zip']
            _phone_number = args['phone_number']
            _poc = args['poc']
            _authinfo = args['authinfo']
            _sites = args['sites']

            query = company_data(company_id=_company_id, company_name=_company_name, street=_street, city=_city,
                                 state=_state, zip=_zip, phone_number=_phone_number, poc=json_decode(_poc),
                                 authinfo=json_decode(_authinfo), sites=json_decode(_sites))
            
            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                    'status' : 200,
                    'message' : 'Company creation successful'
                }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                    'status' : 400,
                    'message' : 'Company creation failure'
                }
        except Exception as e:
            return {'status' : 400}
