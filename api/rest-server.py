#!./flask/bin/python

from flask import Flask, request, jsonify#, abort, make_response, render_template
from flask_restful import Api, Resource, reqparse, fields#, marshal
from _ast import Str
from array import array
#from datetime import datetime, timezone, timedelta
import os
import time
import datetime
#from flask_httpauth import HTTPBasicAuth

#auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

'''http auth
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
'''



@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#@app.route('/api/interface', methods=['GET'])
#def interface():
#    return render_template("interface.html", title = 'interface')

#@app.route('/api/picontroller', methods=['POST', 'GET'])  
#def get(self, id):
#        if id in data['id']:
#    return {'start': data['id'][id]['start'],'end': data['id'][id]['end'],'cmd': data['id'][id]['cmd']}



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
    },
}

#status = {
#    'id': {
#        'glazer': {
#            'online': True,
#            'time': '2016-10-05_22:52:13',
#            'rules': '[]'
#        },
#        'loving': {
#            'online': True,
#            'time': '2016-10-05_22:52:13',
#            'rules': '[]'
#        },
#        'school3': {
#            'online': True,
#            'time': '2016-10-05_22:52:13',
#            'rules': '[]'
#        }
#    },
#} 


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

api.add_resource(timeSync, '/api/picontroller/time')
api.add_resource(piController, '/api/picontroller/<string:id>')
api.add_resource(update, '/api/picontroller/<string:id>/<string:start>/<string:end>/<string:cmd>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6668, debug=False)
