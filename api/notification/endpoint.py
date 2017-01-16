''' username and password needs hidden / parsed from encrypted file '''

from api import app
from api.util.parse_json import *
from api.util.decorator import async
from flask import jsonify, request, json, render_template
from flask_mail import Mail, Message
from flask_restful import Resource, reqparse
import requests, base64, subprocess, os, argparse

# email server config #
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'threatdetectionservice@gmail.com'
app.config['MAIL_PASSWORD'] = 'flyball2011'
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'threatdetectionservice@gmail.com'
app.config['MAIL_DEFAULT_ADMIN'] = ['threatdetectionservice@gmail.com']

# create mail object #
mail = Mail(app)

# define hbase vars #
metronHBaseRestURL="http://10.10.10.154"
metronHbaseRestPort = 9082
metronHBaseTable = "enrichment"
metronHBaseCF="assets"
assetQueryURL =metronHBaseRestURL + ":" + str(metronHbaseRestPort) + "/" + metronHBaseTable 

@async
def send_async_email(app, msg):
    ''' sends mail asynchronously '''
    with app.app_context():
        mail.send(msg)

def send_email(recipients, text_body, html_body=None):
    ''' recipients and text_body are required '''
    
    default_subject = "Threat Notification Service: THREAT DETECTED"
    msg = Message(subject=default_subject, recipients=recipients)
    msg.body = text_body
    if not html_body == None:
        pass
#         msg.html = render_template('email.html', threat_level=threat_level, incident_type=incident_type,
#                         incident_source=incident_source, incident_time=incident_time,
#                         attack_method=attack_method, source=source, destination=destination)
    else:
        msg.html = html_body
    send_async_email(app, msg)
    
class manageNotifications(Resource):
    def post(self):
        ''' post threat notification into an email or sms message and alert users '''
        
        URL = request.url
        
        # send email #
        if URL.find("api/notification/email") > 0:
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('recipients', type=json_encode, location='json')
                parser.add_argument('text_body', type=str, location='json')
                parser.add_argument('html_body', type=str, location='json')
                parser.add_argument('sender', type=str, location='json')
                args = parser.parse_args()
    #             return jsonify(
    #                     subject = args['subject'],
    #                     recipients = json_decode(args['recipients']),
    #                     text_body = args['text_body'],
    #                     html_body = args['html_body'],
    #                     sender = args['sender']
    #                 )
                send_email(args['subject'], json_decode(args['recipients']), args['text_body'], args['html_body'], args['sender'])
                return jsonify(
                        response = 200,
                        message = 'Email delivery success'
                    )
            except Exception as e:
                return {'response' : str(e)}
        
        #send sms
        elif URL.find("api/notification/sms") > 0:
            try:
#                 parser = reqparse.RequestParser()
#                 parser.add_argument('recipients', type=json_encode, location='json')
#                 parser.add_argument('threat_data', type=json_encode, location='json')
#                 args = parser.parse_args()
    #             return jsonify(
    #                     subject = args['subject'],
    #                     recipients = json_decode(args['recipients']),
    #                     text_body = args['text_body'],
    #                     html_body = args['html_body'],
    #                     sender = args['sender']
    #                 )
                
                CWD = os.getcwd()
                script_path = CWD + '/api/notification/flowroute/send_sms.py'
                print("path " + script_path)
                python2_env = {"PYTHONPATH": "/usr/bin/python2.7"}
                subprocess.run("python2.7 " + script_path, env=python2_env, shell=True)
                
                
#               cmd = "python your_program.py -o THIS STRING WILL PRINT"
#               out_str = subprocess.check_output(cmd, shell=True)
#               print(out_str)

                return jsonify(
                        response = 200,
                        message = 'SMS delivery success'
                    )
            except Exception as e:
                return {'response' : str(e)}

    def get(self, threat_id):
        ''' get threat-intel data for threat notification '''
        assetFullQueryURL = assetQueryURL + "/" + threat_id
        print(assetFullQueryURL)
        try:
            response = requests.get(assetFullQueryURL, headers={"Accept" : "application/json"})
            jData = response.json()
        except:
            return "Server Down"
        decodedList  = []
        for row in jData['Row']:
            # Decode the key into ascii #
            #rowKey = base64.b64decode(row['key']).decode('ascii')
            dColumn = {}
            for cell in row['Cell']:
                columnname = base64.b64decode(cell['column']).decode('ascii')
                value = base64.b64decode(cell['$']).decode('ascii')
                dColumn[columnname] = value 
            decodedList.append (dColumn) 
        return jsonify(threat_intel=decodedList)
    
class metronAlerts(Resource):
    def post(self):
        ''' process threat-intel and conditionally alert user as threat notification '''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('score', type=int, location='json')
            parser.add_argument('threat_data', type=json_encode, location='json')
            args = parser.parse_args()
#             return jsonify(
#                     score = args['subject'],
#                     threat_data = json_decode(args['threat_data'])
#                 )
            return jsonify(
                    response = 200,
                    message = 'Email delivery success'
                )
        except Exception as e:
            return {'response' : str(e)}
        
