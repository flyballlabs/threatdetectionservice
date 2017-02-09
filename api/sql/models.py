import json, sqlalchemy, uuid
from api import db, app
from flask_security import RoleMixin
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

# MySQL specific imports #
from sqlalchemy import null, Column
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext import mutable
from sqlalchemy.dialects.mysql import JSON, INTEGER, VARCHAR, TINYINT #, DATE, DATETIME
from flask_table import Table, Col
 
##### classes / methods we may need #######################################
#  from wtforms.validators import mac_address  #    mac address parsing   #
#  from ipaddress import ip_address            #     ip address parsing   #
#  from alembic.util.messaging import status   #       html code status   #
###########################################################################

# Connect to the database and provide a handle #
#db = database.connect()

# null constants #
SQL_NULL = null()  # will *always* insert SQL NULL
JSON_NULL = db.Column(JSON(none_as_null=True))  # will *always* insert JSON string "null"

def serialize(model):
    # get names of all columns in model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # return values in a dict
    return dict((c, getattr(model, c)) for c in columns)

'''Enables JSON storage by encoding and decoding on the fly'''
class JsonEncodedDict(sqlalchemy.TypeDecorator): # easily iterable #
    impl = sqlalchemy.String
    def process_bind_param(self, value, dialect):
        return json.dumps(value)
    def process_result_value(self, value, dialect):
        return json.loads(value)
mutable.MutableDict.associate_with(JsonEncodedDict) # add this datatype to table column #

class user_data(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  #latin1
    }
    
    user_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    username = db.Column(VARCHAR(45),index=True, unique=True, nullable=False)
    firstname = db.Column(VARCHAR(45))
    lastname = db.Column(VARCHAR(45))               ##mysql dialect table format##
    password = db.Column(VARCHAR(45))               #Table('mytable', metadata,  #
    email = db.Column(VARCHAR(45))                  #Column('data', String(32)), #
    company_id = db.Column(INTEGER, nullable=False) #mysql_engine='InnoDB',      #
    active = db.Column(TINYINT)                     #mysql_charset='utf8',       #
    phone_number = db.Column(VARCHAR(45))           #mysql_key_block_size="1024")#
    lastlogin = db.Column(VARCHAR(45))              ##############################
    account_type = db.Column(VARCHAR(45))
    notification = db.Column(JSON)
    password_hash = db.Column(db.String(64)) #TODO: do we need this??
                                           
    def __init__(self, user_id, username, firstname, lastname, password, email, company_id, active, phone_number, lastlogin, account_type, notification):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email
        self.company_id = company_id
        self.active = active
        self.phone_number = phone_number
        self.lastlogin = lastlogin
        self.account_type = account_type
        self.notification = notification

    def __repr__(self):
        return '{user: %r}' % self.user_id

    def get_id(self):
        return str(self.user_id)

     # Will generate a token using the itsdangerous extension
     # The app config variable SECRET_KEY will be used as the secret to generate the token
     # The expiration of the token is set for 600 seconds 
    def generate_auth_token(self, expiration = 600):
        expiration = app.config['TOKEN_EXPIRATION']
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'user_id': self.user_id }) 

# Role class
class Role(db.Model, RoleMixin):

    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)

class facial_image_data(db.Model):
    __tablename__ = 'facial_image'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    facial_image_id = db.Column(VARCHAR(200), primary_key=True, default=lambda: uuid.uuid4().hex)
    company_id = db.Column(VARCHAR(45))
    image_name = db.Column(VARCHAR(100))
    image_http_url = db.Column(VARCHAR(200))
    engine_type = db.Column(VARCHAR(45))
    face_id = db.Column(VARCHAR(100))
    facelist_id = db.Column(VARCHAR(45))

    def __init__(self, company_id, image_name, image_http_url, engine_type, face_id, facelist_id):
        #self.facial_image_id = facial_image_id
        self.company_id = company_id
        self.image_name = image_name
        self.image_http_url = image_http_url
        self.engine_type = engine_type
        self.face_id = face_id
        self.facelist_id = facelist_id

    def __repr__(self):
        return '{facial_image: %r}' % self.facial_image_id

class company_data(db.Model):
    __tablename__ = 'company'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  
    }
    
    company_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    company_name = db.Column(VARCHAR(45), unique=True, nullable=False)
    street = db.Column(VARCHAR(45))
    city = db.Column(VARCHAR(45))
    state = db.Column(VARCHAR(45))
    zip = db.Column(VARCHAR(45))
    phone_number = db.Column(VARCHAR(45))
    poc =  db.Column(JSON)
    authinfo =  db.Column(JSON)
    sites = db.Column(JSON)
    
    def __init__(self, company_id, company_name, street, city, state, zip, phone_number, poc, authinfo, sites):
        self.company_id = company_id
        self.company_name = company_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.phone_number = phone_number
        self.poc = poc
        self.authinfo = authinfo
        self.sites = sites

    def __repr__(self):
        return '{company: %r}' % self.company_id
    
class agent_data(db.Model):
    __tablename__ = 'agent'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  
    }
    
    agent_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    mac_address = db.Column(VARCHAR(45), unique=True, nullable=False)
    ip_address = db.Column(VARCHAR(45))
    active = db.Column(TINYINT)
    company_id = db.Column(INTEGER, nullable=False)
    site = db.Column(VARCHAR(45))
    mode = db.Column(VARCHAR(45))
    cmd = db.Column(VARCHAR(45))
    time_setting = db.Column(JSON) #(sqltypes.JSON)
    
    def __init__(self, agent_id, mac_address, ip_address, active, company_id, site, mode, cmd, time_setting):
        self.agent_id = agent_id
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.active = active
        self.company_id = company_id
        self.site = site
        self.mode = mode
        self.cmd = cmd
        self.time_setting = time_setting

    def __repr__(self):
        return '{agent: %r}' % self.agent_id
