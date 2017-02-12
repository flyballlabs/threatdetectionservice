from api import *
from sqlalchemy_utils import database_exists, create_database

# Setup API routes and start the server

api.add_resource(manageAgent, '/api/agent/<string:_mac_address_>')
api.add_resource(manageAgentList, '/api/agent')

api.add_resource(piController, '/api/picontroller/time', '/api/picontroller/<string:_mac_address_>')

api.add_resource(userAuth, '/api/auth/<string:_username>/<string:_password>')
api.add_resource(userAuthToken, '/api/auth')

api.add_resource(manageUser, '/api/user/<string:_username_>')
api.add_resource(manageUserList, '/api/user')

api.add_resource(manageCompany, '/api/company/<string:_company_name_>')
api.add_resource(manageCompanyList, '/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites')

api.add_resource(metronThreats, '/api/metron/threats/<string:_device_>')
api.add_resource(manageAssets, '/api/assets/<string:_device_>')

api.add_resource(manageNotifications, '/api/notifications/email', '/api/notification/sms', '/api/notification/alerts')

api.add_resource(manageFacial, '/api/facial')
api.add_resource(manageFacialRepo, '/api/facial/images/<string:_customerID_>/repo/<string:_fileName_>')
api.add_resource(manageFacialSearch, '/api/facial/search/<string:_customerID_>/<string:_userID_>', '/api/facial/search/<string:_customerID_>/<string:_userID_>/<string:_fileName_>')

if __name__ == '__main__':
    if not database_exists('mysql://tmp:tmp@127.0.0.1/tmp'):
        create_database('mysql://tmp:tmp@127.0.0.1/tmp')
    db.create_all()
    app.run(host='0.0.0.0', port=7777, debug=False)
