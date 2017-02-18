from flask import Flask, Response, make_response, jsonify 
from flask_restful import Api, reqparse, fields 
from flask_cors import CORS, cross_origin
from flask_login import LoginManager, UserMixin, login_required, utils,login_user
from flask_sqlalchemy import SQLAlchemy

# Define the Application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object
app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'mysql://tmp:tmp@127.0.0.1/tmp')
db = SQLAlchemy(app)

# Import Endpoints

from .auth.endpoint import *
from .user.endpoint import *
from .agent.endpoint import *
from .company.endpoint import *
from .metron.endpoint import *
from .asset.endpoint import *
from .notification.endpoint import *
from .facial.endpoint import *

# Import Models - must be imported prior to starting server
from .sql.models import *


# Define Configurations

app.config['DEBUG'] = True
# SECRET_KEY is used by Flask to encrypt data in the Session object
app.config['SECRET_KEY'] = 'flyball2016'
app.config['TOKEN_EXPIRATION'] = 3600

# DEBUG: show path app is initialized at
# print("root path: {}\ninstance path: {}".format(app.root_path, app.instance_path))

# Define API object based on the app object
api= Api(app)


# Define COR based o the app objet
CORS(app)

# Secret configuration for Flask-Security
# Specify the security has PBKDF2 with salt.
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
# Replace this with your own salt.
app.config['SECURITY_PASSWORD_SALT'] = 'flyball2016' 

# Define the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# user_loader callback - used to load a user by it's id
#@login_manager.user_loader
#def load_user(id):
#    return user_data.query.get(int(id))

@login_manager.request_loader
def load_user_from_request(request):

     #first, try to Login using a token
    token = request.headers.get('X-AUTH-TOKEN')
    if token:
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        #decode the token and then look up the user
        user = user_data.query.get(data['user_id'])
        if user:
            return user

    #next, try to Login using Basic Auth
    basic_auth  = request.headers.get('Authorization')
    if basic_auth:
        basic_auth = basic_auth.replace('Basic ', '', 1)
        try:
            basic_auth = base64.b64decode(basic_auth)
        except TypeError:
            pass
        creds = basic_auth.split(b':')
        _username = creds[0]
        _password = creds[1]
        user = user_data.query.filter_by(username=_username,password=_password).first()
        if user:
             return user
    return None

#@app.before_first_request
#def before_first_request():
#
#    # Create any database tables that don't exist yet.
#    db.create_all()
#
#    # Create the Roles "admin" and "end-user" -- unless they already exist
#    user_datastore.find_or_create_role(name='admin', description='Administrator')
#    user_datastore.find_or_create_role(name='soc-user', description='SOC user')
#
#    encrypted_password = utils.encrypt_password('password')
#    if not user_datastore.get_user('admin@flyballlabs.com'):
#        user_datastore.create_user(email='admin@flyballlabs.com', password=encrypted_password)
#
#    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
#    db.session.commit()
#
#    #Assign the admin use to the admin role
#    user_datastore.add_role_to_user('admin@flyballlabs.com','admin')
#
#    db.session.commit()

# Define the HTTP error handling
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

