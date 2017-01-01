# MySQL specific imports #
from sqlalchemy import null , Column
from sqlalchemy.dialects.mysql import JSON, INTEGER, VARCHAR #, DATE, DATETIME
from flask_security import RoleMixin, UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from api import db
from api import app

##### classes / methods we may need ############
#  from wtforms.validators import mac_address  #
#  from ipaddress import ip_address            #  
#  from alembic.util.messaging import status   #
#  from sqlalchemy.sql import sqltypes         #
################################################

# null constants #
SQL_NULL = null()  # will *always* insert SQL NULL
JSON_NULL = db.Column(JSON(none_as_null=True))  # will *always* insert JSON string "null"

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # get names of all columns in model
  columns = [c.key for c in sqlalchemy.orm.class_mapper(model.__class__).columns]
  # return values in a dict
  return dict((c, getattr(model, c)) for c in columns)

class user_data(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  #latin1
    }
    
    user_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    username = db.Column(VARCHAR(45), unique=True, nullable=False)
    firstname = db.Column(VARCHAR(45))
    lastname = db.Column(VARCHAR(45))      
    password = db.Column(VARCHAR(45))      
    email = db.Column(VARCHAR(45))         
    company_id = db.Column(VARCHAR(45))    
    active = db.Column(VARCHAR(45))        
    lastlogin = db.Column(VARCHAR(45))    
     
                                           
    def __init__(self, user_id, username, firstname, lastname, password, email, company_id, active, lastlogin):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email
        self.company_id = company_id
        self.active = active
        self.lastlogin = lastlogin

    def __repr__(self):
        return '{user: %r}' % self.user_id

    def get_id(self):
        return str(self.user_id)

     # Will generate a token using the itsdangerous extension
     # The app config variable SECRET_KEY will be used as the secret to generate the token
     # The expiration of the token is set for 600 seconds 
    def generate_auth_token(self, expiration = 600):
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
    authinfo =  db.Column(JSON)
    sites = db.Column(JSON)
    
    def __init__(self, company_id, company_name, street, city, state, zip, phone_number, authinfo, sites):
        self.company_id = company_id
        self.company_name = company_name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.phone_number = phone_number
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
    status = db.Column(VARCHAR(45))
    company_id = db.Column(VARCHAR(45))
    site = db.Column(VARCHAR(45))
    mode = db.Column(VARCHAR(45))
    cmd = db.Column(VARCHAR(45))
    time_setting = db.Column(JSON) #(sqltypes.JSON)
    
    def __init__(self, agent_id, mac_address, ip_address, status, company_id, site, mode, cmd, time_setting):
        self.agent_id = agent_id
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.status = status
        self.company_id = company_id
        self.site = site
        self.mode = mode
        self.cmd = cmd
        self.time_setting = time_setting

    def __repr__(self):
        return '{agent: %r}' % self.agent_id
