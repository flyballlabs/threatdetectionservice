import os
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired) #tokens
from flask_restful import Resource, reqparse
from api.sql.models import *  #import all of the models from models.py
from flask import abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth()

#for login page, USER is session object for auth user
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    USER = user_data.verify_auth_token(username_or_token)
    if not USER:
        # try to authenticate with username/password
        USER = user_data.query.filter_by(username=username_or_token).first()
        if not USER or not user_data.verify_password(password):
            return False
    g.user_data = USER
    return True

#redir at here to get a token#
@app.route('/api/auth/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

#verify to protect resources
@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})
        
        
@app.route('/api/users/<int:id>')
def get_userID(id):
    USER = user_data.query.get(id)
    if not USER:
        abort(400)
    return jsonify({'username': USER.username})



'''# hashing functions #
@auth.hash_password
def hash_pw(password):
    return md5(password).hexdigest()

@auth.hash_password
def hash_pw(username, password):
    get_salt(username)
    return hash(password, salt)

@auth.verify_password
def verify_pw(username, password):
    return call_custom_verify_function(username, password)'''

class userAuth(Resource):
    def get(self, _username, _password):
        try:
            x = user_data.query.all()
            table = user_table(x) # Populate the table
            print(table.__html__())
            
            x = user_data.query.filter_by(username=_username).first()
            if x != None:
                if x.password == _password:
                    curr_session = db.session
                    if x.account_type == 'user':
                        x.status = 1
                    elif x.account_type == 'admin':
                        x.status = 2
                    elif x.account_type == 'su':
                        x.status = 3
                    curr_session.commit() #commit changes
                    return {
                            'authentication': True,
                            #auth level: 1 - user, 2 - admin, 3 su
                            'account_type': x.account_type 
                           }
                else:
                    return {
                            'authentication': False,
                            'message':'Authentication failure'
                           }
            else:
                return {
                        'status': 400,
                        'message':'User search failure'
                       }
        except Exception as e:
            curr_session.rollback()
            curr_session.flush()
            return {'error': str(e)}
