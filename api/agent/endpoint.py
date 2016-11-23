#from flask import jsonify
from flask_restful import Resource, reqparse
import time, datetime
from sql.models import *  #import all of the models from models.py
from app.parse_json import * #for json request parsing

'''
## migrate to mysql database ##
data = {
    'id': {
        'glazer': {
            'start': '08:00:00',
            'end': '16:00:00',
            'cmd': '' #'start', 'stop', 'now'
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
'''

class piController(Resource):
    def get(self, id):
        #if id in data['id']:
        return {'start': data['id'][id]['start'],'end': data['id'][id]['end'],'cmd': data['id'][id]['cmd']}
    
    def get(self):
        dtz = timezone(-timedelta(hours=4))
        dtUTC = datetime.now(dtz)
        dtfUTC = datetime.strftime(dtUTC, '%Y-%m-%d %H:%M:%S')
        return dtfUTC
    
class update(Resource):
    def post(self, id, start, end, cmd):
        data['id'][id]['start'] = start
        data['id'][id]['end'] = end
        data['id'][id]['cmd'] = cmd
        return 'UPDATED VALUES For:' + id + os.linesep + 'START:' + start + os.linesep + 'END:' + end + os.linesep + 'CMD:' + cmd

## TODO ##
class manageAgents(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('agent_id', type=int, help='Agent_id for agent', location='json')
            parser.add_argument('mac_address', type=str, help='Mac Address for agent', location='json')
            parser.add_argument('ip_address', type=str, help='IP Address for agent', location='json')
            parser.add_argument('status', type=str, help='Status of agent', location='json')
            parser.add_argument('company_id', type=str, help='Company ID associated with agent', location='json')
            parser.add_argument('site', type=str, help='Site agent is deployed at', location='json')
            parser.add_argument('mode', type=str, help='Mode agent is operating in', location='json')
            parser.add_argument('cmd', type=str, help='Current cmd selection for agent', location='json')
            parser.add_argument('time_setting', type=json_decode, help='Time settings for the agent', location='json')
            args = parser.parse_args()#strict=True

            _agent_id = args['agent_id']
            _mac_address = args['mac_address']
            _ip_address = args['ip_address']
            _status = args['status']
            _company_id = args['company_id']
            _site = args['site']
            _mode = args['mode']
            _cmd = args['cmd']
            _time_setting = args['time_setting']
            
            query = agent_data(agent_id=_agent_id, mac_address=_mac_address, ip_address=_ip_address, 
                              status=_status, company_id=_company_id, site=_site, 
                              mode=_mode, cmd=_cmd, time_setting=_time_setting)

            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared company_idment to opened session
                curr_session.commit() #commit changes
                return  {
                            'status': 200,
                            'message':'Agent creation successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status': 400,
                            'message':'Agent creation failure'
                        }
        except Exception as e:
            return {'error': str(e)}

    def patch(self, _mac_address_):
        try:
            parser = reqparse.RequestParser()
            
            # conditionally replace user data if arg exists #
            parser.add_argument('agent_id', type=int, help='Agent_id for agent', location='json')
            parser.add_argument('mac_address', type=str, help='Mac Address for agent', location='json')
            parser.add_argument('ip_address', type=str, help='IP Address for agent', location='json')
            parser.add_argument('status', type=str, help='Status of agent', location='json')
            parser.add_argument('company_id', type=str, help='Company ID associated with agent', location='json')
            parser.add_argument('site', type=str, help='Site agent is deployed at', location='json')
            parser.add_argument('mode', type=str, help='Mode agent is operating in', location='json')
            parser.add_argument('cmd', type=str, help='Current cmd selection for agent', location='json')
            parser.add_argument('time_setting', type=json_decode, help='Time settings for the agent', location='json')
            
            args = parser.parse_args()#strict=True, require=True
            
            #for response in args:         ############################  
            #    if args[response] != None:# optimize in future release
                
            if args['agent_id'] != None:
                _agent_id = args['agent_id']
            if args['mac_address'] != None:
                _mac_address = args['mac_address']
            if args['ip_address'] != None:
                _ip_address = args['ip_address']
            if args['status'] != None:
                _status = args['status']
            if args['company_id'] != None:
                _company_id = args['company_id']
            if args['site'] != None:
                _site = args['site']
            if args['mode'] != None:
                _mode = args['mode']
            if args['cmd'] != None:
                _cmd = args['cmd']
            if args['time_setting'] != None:
                _time_setting = args['time_setting']
            ###################################
            # would be faster in an array / loop
            
            try:
                curr_session = db.session #open database session
                x = agent_data.query.filter_by(mac_address=_mac_address_).first() #fetch the name to be updated
                x.agent_id = _agent_id   #update the row
                x.mac_address = _mac_address
                x.ip_address = _ip_address
                x.status = _status
                x.company_id = _company_id
                x.site = _site
                x.mode = _mode
                x.cmd = _cmd
                x.time_setting = json_encode(_time_setting)
                curr_session.commit() #commit changes
                
                return  {
                            'status': 200,
                            'message':'Agent update successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status':400,
                            'message':'Agent update failure'
                        }
        except Exception as e:
            return {'error': str(e)}
        
    def get(self, _mac_address_):
        try:
            x = agent_data.query.filter_by(mac_address=_mac_address_).first()
            _agent_id = x.agent_id
            _mac_address = x.mac_address
            _ip_address = x.ip_address
            _status = x.status
            _company_id = x.company_id
            _site = x.site
            _mode = x.mode
            _cmd = x.cmd 
            _time_setting = x.time_setting #json_decode()
            
            if x != None:
                return {
                        'agent_id':_agent_id,
                        'mac_address':_mac_address,
                        'ip_address' : _ip_address,
                        'status' : _status,
                        'site' : _site,
                        'mode' : _mode,
                        'cmd' : _cmd, 
                        'time_setting' : _time_setting #json_encode() / jsonify()
                       }
            else:
                return {
                        'status': 400,
                        'message':'Agent search failure'
                       }
        except Exception as e:
            return {'error': str(e)}
        
    def delete(self, _mac_address_):
        try:
            curr_session = db.session #open database session
            x = agent_data.query.filter_by(mac_address=_mac_address_).first()
            try:
                db.session.delete(x)
                db.session.commit()
                return  {
                            'status': 200,
                            'message':'Agent delete successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'status':400,
                            'message':'Agent delete failure'
                        }
        except Exception as e:
            return {'error': str(e)}