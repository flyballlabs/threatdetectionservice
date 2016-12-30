from api import *

# Setup API routes and start the server

api.add_resource(manageAgent, '/api/agent/<string:_mac_address_>')
api.add_resource(manageAgentList, '/api/agent')

api.add_resource(piController, '/api/picontroller/time', '/api/picontroller/<string:_mac_address_>')

api.add_resource(userAuth, '/api/auth/<string:_username>/<string:_password>')

api.add_resource(manageUser, '/api/user/<string:_username_>')
api.add_resource(manageUserList, '/api/user')

api.add_resource(manageCompany, '/api/company/<string:_company_name_>')
api.add_resource(manageCompanyList, '/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites')

api.add_resource(metronThreats, '/api/metron/threats/<string:_device_>')
api.add_resource(manageAssets, '/api/assets/<string:_device_>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=False)
