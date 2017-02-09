'''
@summary: Handles all notifications for api, including alerts from metron.
Note: Ensure username and password needs hidden / parsed from encrypted file.
@author: devopsec
'''
import sys
import traceback
from api import app, time_funcs
from api.util.parse_json import *
from api.decorators import async
from api.sql.models import user_data
from api.company.endpoint import companyUtils
from flask import jsonify, request, json, render_template
from flask_mail import Mail, Message
from flask_restful import Resource, reqparse
from starbase import Connection
import requests, base64, subprocess, os

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
metronHBaseRestURL = "http://localhost"
metronHbaseRestPort = 9082
metronHBaseTable = "enrichment"
metronHBaseCF = "assets"
apiBaseRestUrl = "http://0.0.0.0:7777"
apiCompanyEndpoint = "/api/company/"
assetQueryURL = metronHBaseRestURL + ":" + str(metronHbaseRestPort) + "/" + metronHBaseTable

# abstraction of email and sms functions
@async
def send_async_email(app, msg):
    ''' sends mail asynchronously '''
    with app.app_context():
        mail.send(msg)

def send_email(recipients, text_body, html_body=None, subject="Threat Notification Service",
               sender="threatdetectionservice@gmail.com", threat_data=None):
    ''' recipients and text_body params are required '''

    # add threat_data if provided
    if not threat_data == None:
        text_body += threat_data

    msg = Message(recipients=recipients, subject=subject, html=html_body, sender=sender)

    if not html_body == None:
        pass
    # TODO finish html template for emails
#       msg.html = render_template('email.html', threat_level=threat_level, incident_type=incident_type,
#                                   incident_source=incident_source, incident_time=incident_time,
#                                   attack_method=attack_method, source=source, destination=destination)
    else:
        pass
        # msg.html = html_body
    send_async_email(app, msg)

@async
def send_sms(to, msg, frm="12485042987", threat_data=None):
    ''' to, frm, and msg params are required '''
    CWD = os.getcwd()
    script_path = os.path.join(CWD, 'notification', 'flowroute', 'send_sms.py')
    # DEBUG
    print("path " + script_path)

    # TODO make path cross-platform compatible
    python2_env = {"PYTHONPATH": "/usr/bin/python2.7"}
    if not threat_data == None:
        msg += threat_data

    # convert to arg into string representation for cmd line
    # toStrList = []
    # for number in to:
    #     toStrList.append(str(number))

    cmd = "python2.7 {0} -t {1} -f {2} -m '{3}'".format(script_path, to, frm, msg)
    print(cmd)
    subprocess.run(cmd, env=python2_env, shell=True)
    #out_str = subprocess.check_output(cmd, shell=True)

    # DEBUG
    # print(cmd)
    # print(out_str)

class manageNotifications(Resource):
    ''' Handles processing of notifications with following functions:
    Post threat notification into an email or sms message and alert users
    Process threat-intel and conditionally alert user as threat notification '''

    threat_data = None # class variable
    contact_info = [] # class variable

    def post(self):
        ''' process a notification '''
        MASS_ALERT_FLAG = False
        URL = request.url

        # process alert #
        if URL.find("api/notifications/alert") > 0:
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('threat_intel', type=dict, location='json')
                args = parser.parse_args()

                if args['threat_intel']['_source']['is_alert'] == "true":

                    # gather necessary info from threat_intel
                    manageNotifications.threat_data = {
                        "index": args['threat_intel']['_index'],
                        "score": args['threat_intel']['_score'],
                        "threat_level": args['threat_intel']['_source']['threat.triage.level'],
                        "source": args['threat_intel']['_source']['source.type'],
                        "ip_src_addr": args['threat_intel']['_source']['ip_src_addr'],
                        "ip_dst_addr": args['threat_intel']['_source']['ip_dst_addr'],
                        "url": args['threat_intel']['_source']['url'],
                        "time": time_funcs.convert_epoch_ts(args['threat_intel']['_source']['timestamp'])
                    }

                    # TODO enrich threat-intel in metron with source company name
                    # TODO check threat_data to find where alert is from (what company)
                    company = "ALL"
                    company = "Flyball-Labs"
                    if company == "ALL": # for alerting all companies, in event of a data breach
                        MASS_ALERT_FLAG = True
                        response = companyUtils.get_all_poc_list()
                    else: # alert a single company
                        response = companyUtils.get_company_poc_list(company)

                    # gather contact info from company & get notification settings for each poc
                    if MASS_ALERT_FLAG == True:
                        if response['status'] == 200:
                            all_poc_list = response['all_company_poc']

                            for co in all_poc_list:
                                for poc in co['poc']:
                                    user = user_data.query.filter_by(username=poc).first()
                                    manageNotifications.contact_info.append({
                                        "name": user.firstname,
                                        "phone": user.phone_number,
                                        "email": user.email,
                                        "alert_type": user.notification['alert_type'],
                                        "notification_type": user.notification['notification_type']
                                    })
                        else:  # could not get poc list
                            return jsonify(
                                status = 400,
                                message = "Could not obtain POC list"
                            )
                    else:
                        if response['status'] == 200:
                            poc_list = response['poc']

                            for poc in poc_list:
                                user = user_data.query.filter_by(username=poc).first()
                                manageNotifications.contact_info.append({
                                    "name": user.firstname,
                                    "phone": user.phone_number,
                                    "email": user.email,
                                    "alert_type": user.notification['alert_type'],
                                    "notification_type": user.notification['notification_type']
                                })
                        else: # could not get poc list
                            return jsonify(
                                status = 400,
                                message = "Could not obtain POC list"
                            )

                    # iterate through contact info and send message if score >= user setting
                    for contact in manageNotifications.contact_info:
                        if manageNotifications.threat_data['score'] >= contact['alert_type']:
                            if contact['notification_type'] == "email":
                                send_email(recipients=[contact['email']],
                                           text_body="Hello " + contact['name'] + ",\n\nThere was a threat detected on your network at " +
                                                     manageNotifications.threat_data['time'] + "\nA summary of the details are provided below.\n" +
                                                     "For more information, login to your account, and view the ThreatDetection Service Dashboard.\n",
                                           threat_data=json_encode(manageNotifications.threat_data))
                            elif contact['notification_type'] == "sms":
                                send_sms(to=contact['phone'],
                                         msg="Hello " + contact['name'] + ",\n\nThere was a threat detected on your network at " +
                                             manageNotifications.threat_data['time'] + "\nA summary of the details are provided below.\n" +
                                             "For more information, login to your account, and view the ThreatDetection Service Dashboard.\n",
                                         threat_data=json_encode(manageNotifications.threat_data))

                return jsonify(
                    status = 200,
                    message = "Alert parsing successful"
                )

            except Exception as e:
                # DEBUG only (security risk : TMI)
                print("Unexpected error:", sys.exc_info()[0]) # sys info
                print(type(e))  # the exception instance
                print(e.args)  # arguments stored in .args
                print(e)  # the actual error
                traceback.print_tb(e.__traceback__) # print stack trace

        # send email #
        if URL.find("api/notification/email") > 0:
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('recipients', type=list, location='json')
                parser.add_argument('subject', type=str, location='json')
                parser.add_argument('text_body', type=str, location='json')
                parser.add_argument('html_body', type=str, location='json')
                parser.add_argument('sender', type=str, location='json')
                args = parser.parse_args()

                # DEBUG
                # return jsonify(
                #     subject = args['subject'],
                #     recipients = args['recipients'],
                #     text_body = args['text_body'],
                #     html_body = args['html_body'],
                #     sender = args['sender']
                # )

                send_email(args['subject'], args['recipients'], args['text_body'],
                           args['html_body'], args['sender'])

                return jsonify(
                        status = 200,
                        message = 'Email delivery success'
                    )
            except Exception as e:
                return {'error' : str(e)} # DEBUG only (security risk : TMI)
        
        #send sms
        elif URL.find("api/notification/sms") > 0:
            try:
                parser = reqparse.RequestParser()
                parser.add_argument('to', type=str, location='json')
                parser.add_argument('frm', type=str, location='json')
                parser.add_argument('msg', type=str, location='json')
                args = parser.parse_args()

                # DEBUG
                # return jsonify(
                #     to = json_decode(args['to']),
                #     frm = args['frm'],
                #     msg = args['msg']
                # )

                send_sms(to=args['to'], frm=args['frm'], msg=args['msg'])

                return jsonify(
                    status = 200,
                    message = 'SMS delivery success'
                )
            except Exception as e:
                return {'error' : str(e)} # DEBUG only (security risk : TMI)

    #TODO: could be used if we store notifications in mysql db
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

#TODO: this is redundant and is accomplished in above routines
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
                    status = 200,
                    message = 'Email delivery success'
                )
        except Exception as e:
            return {'status' : str(e)}
