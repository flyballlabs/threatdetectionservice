import database
# MySQL specific imports #
from sqlalchemy import null
from sqlalchemy.dialects.mysql import JSON, INTEGER, VARCHAR #, DATE, DATETIME

# Connect to the database and provide a handle #
db = database.connect()
# null constants #
SQL_NULL = null()  # will *always* insert SQL NULL
JSON_NULL = db.Column(JSON(none_as_null=True))  # will *always* insert JSON string "null"

class user_data(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(INTEGER, primary_key=True)
    username = db.Column(VARCHAR(45), unique=True)
    firstname = db.Column(VARCHAR(45))
    lastname = db.Column(VARCHAR(45))
    password = db.Column(VARCHAR(45))
    email = db.Column(VARCHAR(45), unique=True)
    company_id = db.Column(VARCHAR(45))
    status = db.Column(VARCHAR(45))
    lastlogin = db.Column(VARCHAR(45))

    def __init__(self, user_id, username, firstname, lastname, password, email, company_id, status, lastlogin):
        self.user_id = user_id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.email = email
        self.company_id = company_id
        self.status = status
        self.lastlogin = lastlogin

    def __repr__(self):
        return '{user: %r}' % self.user_id


class company_data(db.Model):
    __tablename__ = 'company'
    company_id = db.Column(INTEGER, primary_key=True)
    name = db.Column(VARCHAR(45), unique=True)
    address = db.Column(VARCHAR(45))
    city = db.Column(VARCHAR(45))
    state = db.Column(VARCHAR(45))
    zip = db.Column(VARCHAR(45))
    phone_number = db.Column(VARCHAR(45))
    authinfo = db.Column(JSON)
    sites = db.Column(db.JSON)

    def __init__(self, company_id, name, address, city, state, zip, phone_number, authinfo, sites):
        self.company_id = company_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone_number = phone_number
        self.authinfo = authinfo
        self.sites = sites

    def __repr__(self):
        return '{company: %r}' % self.company_id