'''
@Summary: Server for GUI pages and user navigation throughout site
@Author: mackhendricks
'''
from gui import app
import requests, json
from flask import current_app, has_request_context
from api.util import dynamic
from gui.util.error_handling import *
from gui.util import classes, configurations
from flask import Flask, render_template, request, jsonify, make_response, abort

# Set configurations and hand off sensitive data to GUI_MAN
status = configurations.set_api_url()
if status == -1:
    print("API Server has NOT been started!")
else:
    print("API Server has been started!")

GUI_MAN = classes.GUI(api_server_url=app.config['API_SERVER_URL'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = GUI_MAN.get_api_server_url() + "/api/auth/" + username + "/" + password

        # exceptions handled by error handlers #
        __headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=__headers)
        jData = response.json()

        # try:
        # always check status from api first #
        if not 'status' in jData:
            print("500")
            raise InvalidLogin(status_code=500)
        elif jData['status'] == 401:
            print("401")
            raise InvalidLogin(status_code=401)
        elif jData['status'] == 403:
            print("403")
            raise InvalidLogin(status_code=403)
        elif jData['status'] == 404:
            print("404")
            raise InvalidLogin(status_code=404)
        elif jData['status'] != 200:
            print("unknown")
            raise InvalidLogin(status_code=jData['status'])
        # except Exception as e:
        #     print(str(e))

        try: # if auth succeeded
            if jData['authentication'] == True:
                GUI_MAN.set_user_name(username)
                resp = make_response(render_template('dashboard.html', username=GUI_MAN.get_user_name(),
                                                     apiServer=GUI_MAN.get_api_server_url(),
                                                     authToken=jData['X-AUTH-TOKEN']))
                resp.set_cookie('X-AUTH-TOKEN', jData['X-AUTH-TOKEN'])
                return resp
        except Exception as e:
            error = "Problem occurred while attempting to login.\nFor help with this error, contact support and provide the following error code:\n{}".format(str(e))
            return render_template('error.html', error=error)

        print("abort")
        abort(401) # if auth failed

    elif (request.method == 'GET'):
        return render_template('login.html', error=error)
    else:
        error = "Request method {} is not supported on this page.".format(request.method)
        return render_template('error.html', error=error)

@app.route('/logout', methods=['GET'])
def logout():
    GUI_MAN.set_user_name(user_name=None)
    resp = make_response(render_template('login.html'))
    resp.set_cookie('X-AUTH-TOKEN', '', expires=0)
    return resp

@app.route('/threats', methods=['GET'])
def threats():
    # Grab the company info
    try:
        url = GUI_MAN.get_api_server_url() + "/api/user/" + GUI_MAN.get_user_name()
        params = request.args.items()

        __headers = {"X-AUTH-TOKEN": getAuthToken(),'Content-Type': 'application/json'}
        response = requests.get(url, headers=__headers, params=params)
        jData = response.json()
        company = jData['company_id']

        site = request.args.get('site')
        url = GUI_MAN.get_api_server_url() + '/api/company/' + str(company) + "/sites"

        # DEBUG
        # print("jData: {}\ncompany: {}\nurl2: {}".format(jData, company, url))

        __headers = {"X-AUTH-TOKEN": getAuthToken(),'Content-Type': 'application/json'}
        response = requests.get(url, headers=__headers, params=params)

        # DEBUG
        # print("response: {}".format(response.json()))

        jData = response.json()
        sites = jData['sites']

        # DEBUG
        # print("jData: {}\nsites: {}\nsite: {}".format(jData, sites, site))

        if (response.status_code != requests.codes.ok):
            error = "Your session has expired or some other issue occurred.  Please try to login again."
            return render_template('login.html', error=error)

        if request.method == 'GET' and site != None:
            threatsBySiteURI = '/api/metron/threats/' + site
            assetURI = '/api/assets/' + site
            authToken = getAuthToken()
            return render_template('threats-by-site.html', username=GUI_MAN.get_user_name(), sites=sites, selectedSite=site,
                                   apiServer=GUI_MAN.get_api_server_url(), authToken=authToken, threatsBySiteURI=threatsBySiteURI, assetURI=assetURI)
        return render_template('threats-by-site.html', sites=sites, username=GUI_MAN.get_user_name())

    except requests.exceptions.RequestException as e:
        error = "Problem occurred while accessing threat information. Please provide this error code to support: \n" + str(e)
        return render_template('error.html', error=error)
    except Exception as e:
        error = "Problem occurred while accessing threat information. Please provide this error code to support: \n" + str(e)
        return render_template('error.html', error=error)

# current version
@app.route('/agent-table', methods=['GET'])
def agent_management():
    co_agents = []
    if not GUI_MAN.get_user_name() == None:
        try:
            url = GUI_MAN.get_api_server_url() + "/api/user/" + GUI_MAN.get_user_name()
            params = request.args.items()

            __headers = {"X-AUTH-TOKEN": getAuthToken(), 'Content-Type': 'application/json'}
            response = requests.get(url, headers=__headers, params=params)
            jData = response.json()
            co_id = jData['company_id']

            url = GUI_MAN.get_api_server_url() + "/api/agent"
            response = requests.get(url, headers=__headers, params=params)
            jData = response.json()
            agent_list = jData['agent_list']

            for agent in agent_list:
                if agent['company_id'] == co_id:
                    print("adding to agent list: {}".format(agent))
                    co_agents.append(agent)

        except requests.exceptions.RequestException as e:
            error = "Problem occurred while accessing agent information. Please provide this error code to support: \n" + str(e)
            return render_template('error.html', error=error)
        except Exception as e:
            error = "Problem occurred while accessing agent information. Please provide this error code to support: \n" + str(e)
            return render_template('error.html', error=error)
        return render_template('agent-table.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken(), agents=co_agents)
    else:
        error = "Your session has expired.. Please log into your account.\n"
        return render_template('login.html', error=error)

# modified version
@app.route('/agent-table-ver2', methods=['GET'])
def agent_management_ver2():
    co_agents = []
    if not GUI_MAN.get_user_name() == None:
        try:
            url = GUI_MAN.get_api_server_url() + "/api/user/" + GUI_MAN.get_user_name()
            params = request.args.items()

            __headers = {"X-AUTH-TOKEN": getAuthToken(), 'Content-Type': 'application/json'}
            response = requests.get(url, headers=__headers, params=params)
            jData = response.json()
            co_id = jData['company_id']

            url = GUI_MAN.get_api_server_url() + "/api/agent"
            response = requests.get(url, headers=__headers, params=params)
            jData = response.json()
            agent_list = jData['agent_list']

            for agent in agent_list:
                if agent['company_id'] == co_id:
                    print("adding to agent list: {}".format(agent))
                    co_agents.append(agent)

        except requests.exceptions.RequestException as e:
            error = "Problem occurred while accessing agent information. Please provide this error code to support: \n" + str(e)
            return render_template('error.html', error=error)
        except Exception as e:
            error = "Problem occurred while accessing agent information. Please provide this error code to support: \n" + str(e)
            return render_template('error.html', error=error)
        return render_template('agent-table-ver2.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken(), agents=co_agents)
    else:
        error = "Your session has expired.. Please log into your account.\n"
        return render_template('login.html', error=error)

# modified version
@app.route('/agent-table-ver3', methods=['GET'])
def agent_management_ver3():
    co_agents = []
    if not GUI_MAN.get_user_name() == None:
        try:
            url = GUI_MAN.get_api_server_url() + "/api/user/" + GUI_MAN.get_user_name()
            params = request.args.items()

            __headers = {"X-AUTH-TOKEN": getAuthToken(), 'Content-Type': 'application/json'}
            response = requests.get(url, headers=__headers, params=params)
            jData = response.json()
            co_id = jData['company_id']

            url = GUI_MAN.get_api_server_url() + "/api/agent"
            response = requests.get(url, headers=__headers, params=params)
            jData = response.json()
            agent_list = jData['agent_list']

            for agent in agent_list:
                if agent['company_id'] == co_id:
                    print("adding to agent list: {}".format(agent))
                    co_agents.append(agent)

        except requests.exceptions.RequestException as e:
            error = "Problem occurred while accessing agent information. Please provide this error code to support: \n" + str(e)
            return render_template('error.html', error=error)
        except Exception as e:
            error = "Problem occurred while accessing agent information. Please provide this error code to support: \n" + str(e)
            return render_template('error.html', error=error)
        return render_template('agent-table-ver3.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken(), agents=co_agents)
    else:
        error = "Your session has expired.. Please log into your account.\n"
        return render_template('login.html', error=error)

# TODO: move responsibility of getting token to GUI_MAN
# Get the Auth Token from the Cookie
def getAuthToken():
    authToken = request.cookies.get('X-AUTH-TOKEN')
    return authToken

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken())

@app.route('/userprofile', methods=['GET'])
def userprofile():
    return render_template('user-profile.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken())

@app.route('/alert-settings', methods=['GET'])
def alert_settings():
    return render_template('alert-settings.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken())

@app.route('/agent-settings', methods=['POST'])
def agent_settings():
    agent_to_edit = request.form['agentMAC']
    print("Agent selected to edit: {}".format(agent_to_edit))
    if agent_to_edit == None: # if doesn't exist
        error = "Problem occurred while accessing agent information.\n"
        return render_template('error.html', error=error)
    return render_template('agent-settings.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken(), agent=agent_to_edit)

    # Used with other variations of agent table #
    # response = make_response(render_template('agent-settings.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(),
    #                                      authToken=getAuthToken(), AGENT=agent_to_edit), 200)
    # response.headers = {'Content-Type': 'text/html, application/json', 'Accept' : 'application/json, text/javascript', 'Connection': 'keep-alive'}
    # return response

@app.route('/facial-upload', methods=['GET'])
def facial_paste():
    return render_template('facial.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(),authToken=getAuthToken())

@app.route('/facial-paste', methods=['GET'])
def facial():
    return render_template('facial-paste.html', username=GUI_MAN.get_user_name(), apiServer=GUI_MAN.get_api_server_url(), authToken=getAuthToken())


if __name__=='__main__':
    app.run(host="0.0.0.0", port=8888, debug=False)
