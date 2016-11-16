#!/usr/bin/python3.5

from flask import Flask, request, jsonify#, abort, make_response, render_template
from flask_restful import Api, Resource, reqparse, fields#, marshal
from flask_sqlalchemy import SQLAlchemy
from array import array
from datetime import datetime, timezone, timedelta
import os
#from flask_httpauth import HTTPBasicAuth

#auth = HTTPBasicAuth()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://tmp:tmp@127.0.0.1/tmp'
# Create SQLAlchemy object
db = SQLAlchemy(app)
# Create API object
api = Api(app)

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    firstname = db.Column(db.String(45))
    lastname = db.Column(db.String(45))
    password = db.Column(db.String(45))
    email = db.Column(db.String(45), unique=True)
    company_id = db.Column(db.String(45))
    status = db.Column(db.String(45))
    lastlogin = db.Column(db.String(45))

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
'''
user_data = {
    'id': {
        'bob1234@gmail.com': {
            'pw': '1234'
        },
        'jessica1234@yahoo.com': {
            'pw': '1234'
        },
        'fred1234@gmail.com': {
            'start': '1234'
        }
    }
}
'''
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

data = {
    'id': {
        'glazer': {
            'start': '08:00:00',
            'end': '16:00:00',
            'cmd': ''#'start', 'stop', 'now'
        },
        'loving': {
            'start': '08:00:00',
            'end': '16:00:00',
            'cmd': ''
        },
        'school3': {
            'start': '08:00:00',
            'end': '16:00:00',
            'cmd': ''
        }
    }
}


class timeSync(Resource):
    def get(self):
        dtz = timezone(-timedelta(hours=4))
        dtUTC = datetime.now(dtz)
        dtfUTC = datetime.strftime(dtUTC, '%Y-%m-%d %H:%M:%S')
        return dtfUTC 

class piController(Resource):
    def get(self, id):
        #if id in data['id']:
        return {'start': data['id'][id]['start'],'end': data['id'][id]['end'],'cmd': data['id'][id]['cmd']}
    
class update(Resource):
    def post(self, id, start, end, cmd):
        data['id'][id]['start'] = start
        data['id'][id]['end'] = end
        data['id'][id]['cmd'] = cmd
        return 'UPDATED VALUES For:' + id + os.linesep + 'START:' + start + os.linesep + 'END:' + end + os.linesep + 'CMD:' + cmd

class user_auth(Resource):
    def get(self, user_name, user_pw):
        x = user.query.filter_by(username=user_name)
        if x != None:
            if x.password == user_pw:
                return {'authentication': True}
            else:
                return {'authentication': False}
        else:
            return {'error': 'Not a valid username'}

api.add_resource(timeSync, '/api/picontroller/time')
api.add_resource(piController, '/api/picontroller/<string:id>')
api.add_resource(update, '/api/picontroller/<string:id>/<string:start>/<string:end>/<string:cmd>')
api.add_resource(user_auth, '/api/auth/<string:user_name>/<string:user_pw>')

if __name__ == '__main__':
    app.run(host='10.10.10.142', port=6668, debug=False)
