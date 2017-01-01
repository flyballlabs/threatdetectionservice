from flask import jsonify, request
from flask_restful import Resource, reqparse
from datetime import datetime, timezone, timedelta
from api.sql.models import *  #import all of the models from models.py
from api.util.parse_json import json_decode, json_encode #for json request parsing
from api import *

## for agent-ops ##
class piController(Resource):
    def get(self, _mac_address_=None):
        URL = request.url
        
        # time sync
        if URL.find("api/picontroller/time") > 0 and _mac_address_ == None:
            try:
                dtz = timezone(-timedelta(hours=4))
                dtUTC = datetime.now(dtz)
                dtfUTC = datetime.strftime(dtUTC, '%Y-%m-%d %H:%M:%S')
                
                return jsonify(
                    response = 200,
                    datetime = dtfUTC
                )
            except Exception as e:
                return {'response' : 400}
        
        # get agent settings
        elif URL.find("api/picontroller") > 0 and _mac_address_ != None:
            try:
                x = agent_data.query.filter_by(mac_address=_mac_address_).first()
                _mode = x.mode
                _cmd = x.cmd 
                _time_setting = x.time_setting #json_decode()
                
                if x != None:
                    return jsonify(
                        response = 200,
                        mode = _mode,
                        cmd = _cmd, 
                        time_setting = _time_setting  #jsonify() json_encode() 
                    )
                else:
                    return {'response' : 400}
            except Exception as e:
                return {'response' : 400}
        else:
            return {'response' : 404}

    @login_required
    def post(self, _mac_address_): # update ip / status
        try:    
            parser = reqparse.RequestParser()
            parser.add_argument('ip_address', type=str, location='json')
            parser.add_argument('status', type=str, location='json')
            args = parser.parse_args()
            
            _ip_address = args['ip_address']
            _status = args['status']
            
            try:
                curr_session = db.session #open database session
                x = agent_data.query.filter_by(mac_address=_mac_address_).first() #fetch the agent to be updated
                x.ip_address = _ip_address # update the row
                x.status = _status
                curr_session.commit() #commit changes
                
                return  {
                            'response': 200,
                            'message' : 'Agent update successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'response' : 400,
                            'message' : 'Agent update failure'
                        }
        except Exception as e:
            return {'response' : 400}

class manageAgent(Resource):
    @login_required
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
            _time_setting = x.time_setting
            #return {'time_setting' : json_encode(_time_setting)}
        
            if x != None:
                return jsonify(
                    response = 200,
                    agent_id = _agent_id,
                    mac_address = _mac_address,
                    ip_address = _ip_address,
                    status = _status,
                    company_id = _company_id,
                    site = _site,
                    mode = _mode,
                    cmd = _cmd, 
                    time_setting = _time_setting 
                )
            else:
                return {
                        'response' : 400,
                        'message' : 'Agent search failure'
                       }
        except Exception as e:
            return {'response' : 400}
    
    @login_required
    def put(self, _mac_address_):
        try:
            parser = reqparse.RequestParser()
            
            # conditionally replace agent data if arg exists #
            parser.add_argument('agent_id', type=int, help='Agent_id for agent', location='json')
            parser.add_argument('ip_address', type=str, help='IP Address for agent', location='json')
            parser.add_argument('status', type=str, help='Status of agent', location='json')
            parser.add_argument('company_id', type=str, help='Company ID associated with agent', location='json')
            parser.add_argument('site', type=str, help='Site agent is deployed at', location='json')
            parser.add_argument('mode', type=str, help='Mode agent is operating in', location='json')
            parser.add_argument('cmd', type=str, help='Current cmd selection for agent', location='json')
            parser.add_argument('time_setting', type=json_encode, help='Time settings for the agent', location='json')
            
            args = parser.parse_args()#strict=True, require=True

            #for response in args:         ############################  
            #    if response != None:# optimize in future release
                
            ##################### would be faster in an array / loop
            #return jsonify(encoded = _time_setting, decoded = json_decode(_time_setting))
            
            try:
                curr_session = db.session #open database session
                x = agent_data.query.filter_by(mac_address=_mac_address_).first() #fetch the agent to be updated
                if args['agent_id'] != None:
                    x.agent_id = args['agent_id']
                if args['ip_address'] != None:
                    x.ip_address = args['ip_address']
                if args['status'] != None:
                    x.status = args['status']
                if args['company_id'] != None:
                    x.company_id = args['company_id']
                if args['site'] != None:
                    x.site = args['site']
                if args['mode'] != None:
                    x.mode = args['mode']
                if args['cmd'] != None:
                    x.cmd = args['cmd']
                if args['time_setting'] != None:
                    x.time_setting = json_decode(args['time_setting'])
                curr_session.commit() #commit changes
                
                return  {
                            'response' : 200,
                            'message' : 'Agent update successful'
                        }
            except Exception as ex:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'response' : 400,
                            'message' : 'Agent update failure'
                        }
        except Exception as e:
            return {'response' : 400}
    
    @login_required
    def delete(self, _mac_address_):
        try:
            curr_session = db.session #open database session
            x = agent_data.query.filter_by(mac_address=_mac_address_).first()
            try:
                db.session.delete(x)
                db.session.commit()
                return  {
                            'response' : 200,
                            'message' : 'Agent delete successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'response' : 400,
                            'message' : 'Agent delete failure'
                        }
        except Exception as e:
            return {'response' : 400}

class manageAgentList(Resource):
    @login_required
    def get(self):
        try:
            x = agent_data.query.all()
            if x != None:
                results = []
                for agent in x:
                    results.append( {
                        'agent_id' : agent.agent_id,
                        'mac_address' : agent.mac_address,
                        'ip_address' : agent.ip_address,
                        'status' : agent.status,
                        'company_id' : agent.company_id,
                        'site' : agent.site,
                        'mode' : agent.mode,
                        'cmd' : agent.cmd, 
                        'time_setting' : agent.time_setting #json_encode() / jsonify()
                    } )
                            
                return jsonify(
                    response = 200,
                    agent_list = results
                )
            else:
                return {
                        'response' : 400,
                        'message' : 'Agent search failure'
                       }
        except Exception as e:
            return {'response' : 400}
    
    @login_required
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
            parser.add_argument('time_setting', type=json_encode, help='Time settings for the agent', location='json')
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
                              mode=_mode, cmd=_cmd, time_setting=json_decode(_time_setting))

            curr_session = db.session #open database session
            try:
                curr_session.add(query) #add prepared statement to opened session
                curr_session.commit() #commit changes
                return  {
                            'response' : 200,
                            'message' : 'Agent creation successful'
                        }
            except:
                curr_session.rollback()
                curr_session.flush() # for resetting non-commited .add()
                return  {
                            'response' : 400,
                            'message' : 'Agent creation failure'
                        }
        except Exception as e:
            return {'response' : 400}
