from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired) #tokens
from api import database
# MySQL specific imports #
from sqlalchemy import null #, Column
from sqlalchemy.dialects.mysql import JSON, INTEGER, VARCHAR #, DATE, DATETIME
from flask_table import Table, Col 
from passlib.apps import custom_app_context as pwd_context
 
##### classes / methods we may need #######################################
#  from sqlalchemy.sql import sqltypes         #  contains sqltypes.JSON  #
#  from wtforms.validators import mac_address  #    mac address parsing   #
#  from ipaddress import ip_address            #     ip address parsing   #
#  from alembic.util.messaging import status   #       html code status   #
###########################################################################

# Connect to the database and provide a handle #
db = database.connect()
# null constants #
SQL_NULL = null()  # will *always* insert SQL NULL
JSON_NULL = db.Column(JSON(none_as_null=True))  # will *always* insert JSON string "null"


class user_data(db.Model):
    __tablename__ = 'user'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  #latin1
    }
    
    user_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    username = db.Column(VARCHAR(45),index=True, unique=True, nullable=False)
    firstname = db.Column(VARCHAR(45))
    lastname = db.Column(VARCHAR(45))      ##mysql dialect table format##
    password = db.Column(VARCHAR(45))      #Table('mytable', metadata,  #
    email = db.Column(VARCHAR(45))         #Column('data', String(32)), #
    company_id = db.Column(VARCHAR(45))    #mysql_engine='InnoDB',      #
    status = db.Column(VARCHAR(45))        #mysql_charset='utf8',       #
    phone_number = db.Column(VARCHAR(45))  #mysql_key_block_size="1024")#
    lastlogin = db.Column(VARCHAR(45))     ##############################
    account_type = db.Column(VARCHAR(45))
    notification = db.Column(VARCHAR(100))
    password_hash = db.Column(db.String(64))
    
    def __init__(self, user_id, username, firstname, lastname, password, email, company_id, status, phone_number, lastlogin, account_type, notification):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email
        self.company_id = company_id
        self.status = status
        self.phone_number = phone_number
        self.lastlogin = lastlogin
        self.account_type = account_type
        self.notification = notification

    def __repr__(self):
        return '{user: %r}' % self.user_id
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(db.app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(db.app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = user_data.query.get(data['id'])
        return user

class user_table(Table):
    classes = ['table', 'table-bordered'] #html class assignment
    user_id = Col('user_id')
    username = Col('username')
    firstname = Col('firstname')
    lastname = Col('lastname')
    password = Col('password')
    email = Col('email')
    company_id = Col('company_id')
    status = Col('status')
    phone_number = Col('phone_number')
    lastlogin = Col('lastlogin')
    account_type = Col('account_type')
    notification = Col('notification')
    

class company_data(db.Model):
    __tablename__ = 'company'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  
    }
    
    company_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    company_name = db.Column(VARCHAR(45), unique=True, nullable=False)
    address = db.Column(VARCHAR(45))
    city = db.Column(VARCHAR(45))
    state = db.Column(VARCHAR(45))
    zip = db.Column(VARCHAR(45))
    phone_number = db.Column(VARCHAR(45))
    poc = db.Column(VARCHAR(100), nullable=False) #JSON
    authinfo =  db.Column(VARCHAR(100)) #JSON
    sites = db.Column(VARCHAR(100)) #JSON
    
    def __init__(self, company_id, company_name, address, city, state, zip, phone_number, poc, authinfo, sites):
        self.company_id = company_id
        self.company_name = company_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone_number = phone_number
        self.poc = poc
        self.authinfo = authinfo
        self.sites = sites

    def __repr__(self):
        return '{company: %r}' % self.company_id

class company_table(Table):
    classes = ['table', 'table-bordered'] #html class assignment
    company_id = Col('company_id')
    company_name = Col('company_name')
    address = Col('address')
    city = Col('city')
    state = Col('state')
    zip = Col('zip')
    phone_number = Col('phone_number')
    poc = Col('poc')
    authinfo = Col('authinfo')
    sites = Col('sites')
    

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
    time_setting = db.Column(VARCHAR(100)) #JSON
    
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
    
class agent_table(Table):
    classes = ['table', 'table-bordered'] #html class assignment
    agent_id = Col('agent_id')
    mac_address = Col('mac_address')
    ip_address = Col('ip_address')
    status = Col('status')
    company_id = Col('company_id')
    site = Col('site')
    mode = Col('mode')
    cmd = Col('cmd')
    time_setting = Col('time_setting')
    
    
class asset_data(db.Model):
    __tablename__ = 'assets'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  
    }
    
    asset_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    company_name = db.Column(VARCHAR(45), nullable=False)
    site = db.Column(VARCHAR(45), nullable=False)
    asset_ip = db.Column(VARCHAR(45))
    asset_mac = db.Column(VARCHAR(45))
    asset_type = db.Column(VARCHAR(45))
    asset_os = db.Column(VARCHAR(45))
    asset_os_info = db.Column(VARCHAR(45))
    
    def __init__(self, asset_id, company_name, site, asset_ip, asset_mac, asset_type, asset_os, asset_os_info):
        self.asset_id = asset_id
        self.company_name = company_name
        self.site = site
        self.asset_ip = asset_ip
        self.asset_mac = asset_mac
        self.asset_type = asset_type
        self.asset_os = asset_os
        self.asset_os_info = asset_os_info

    def __repr__(self):
        return '{asset: %r}' % self.asset_id
    
class asset_table(Table):
    classes = ['table', 'table-bordered'] #html class assignment
    asset_id = Col('asset_id')
    company_name = Col('company_name')
    site = Col('site')
    asset_ip = Col('asset_ip')
    asset_mac = Col('asset_mac')
    asset_type = Col('asset_type')
    asset_os = Col('asset_os')
    asset_os_info = Col('asset_os_info')


class notification_data(db.Model):
    __tablename__ = 'notifications'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  
    }
    
    notification_id = db.Column(INTEGER, primary_key=True, unique=True, nullable=False)
    company_name = db.Column(VARCHAR(45), nullable=False)
    site = db.Column(VARCHAR(45))
    message = db.Column(VARCHAR(100))
    
    def __init__(self, notification_id, company_name, site, message):
        self.notification_id = notification_id
        self.company_name = company_name
        self.site = site
        self.message = message

    def __repr__(self):
        return '{notification: %r}' % self.notification_id
    
class notification_table(Table):
    classes = ['table', 'table-bordered'] #html class assignment
    notification_id = Col('notification_id')
    company_name = Col('company_name')
    site = Col('site')
    message = Col('message')
    