'''
@Summary: Server for GUI pages and user navigation throughout site
@Author: mackhendricks
'''

import requests, json
from flask import Flask, render_template, request, jsonify, make_response
from  api.util import dynamic

app = Flask(__name__)

# Configurations
app.config.from_object('config')

if ('API_SERVER_URL' in app.config) and len(app.config['API_SERVER_URL']) > 0:
    API_SERVER = app.config['API_SERVER_URL']
else: #Assume the the server is located on the local server
    ip = dynamic.get_current_ip()
    API_SERVER = "http://{}:7777".format(ip)
    app.config['API_SERVER_URL'] = API_SERVER

print("API Server:" + API_SERVER) # Print the API Server URL on the console

# TODO: Define what vars to store here, API_SERVER isn't really sensitive data but username is
class GUI:
    ''' Container for encapsulation / data-hiding of configuration variables.
        Variables that are sensitive but used during operation, load here.
        GUI is created when gui_server.py starts and destroyed on shut down. '''

    def __init__(self, user_name=None, api_server_url=None):
        self.__user_name = user_name
        self.__api_server_url = api_server_url
        print("GUI configuration variables initialized")

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def get_user_name(self):
        return self.__user_name

    def set_api_server_url(self, api_server_url):
        self.__api_server_url = api_server_url

    def get_api_server_url(self):
        return self.__api_server_url

    def __repr__(self):
        if self.__user_name == None or self.__api_server_url == None:
            return "GUI Not Valid"
        return "GUI Valid"

    def __del__(self):
        self.__user_name = ""
        self.__api_server_url = ""
        print("GUI configuration variables destroyed")

GUI_MAN = GUI(api_server_url=API_SERVER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = API_SERVER + "/api/auth/" + username + "/" + password
        apiServer = app.config['API_SERVER_URL']
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            error = "Make sure the API Server is started and then try to login again"
            return render_template('login.html',error=error)
        jData = response.json()
        if jData['authentication'] == True:
            GUI_MAN.set_user_name(username)
            resp = make_response(render_template('dashboard.html', username=GUI_MAN.get_user_name(), apiServer=apiServer, authToken=jData['X-AUTH-TOKEN']))
            resp.set_cookie('X-AUTH-TOKEN',jData['X-AUTH-TOKEN'])
            return resp
        else:
            error = "Username or Password was not correct"

    return render_template('login.html',error=error)


@app.route('/logout', methods=['GET'])
def logout():
    GUI_MAN.set_user_name(user_name=None)
    resp = make_response(render_template('login.html'))
    resp.set_cookie('X-AUTH-TOKEN', '', expires=0)
    return resp	 

@app.route('/threats', methods=['GET'])
def threats():
    # TODO: make these vars dynamic (grab company from api on login?)
    company = "Flyball-Labs"
    # Grab the sites for the company
    url =  API_SERVER  + '/api/company/' + company + "/sites"
    params = request.args.items()
    site = request.args.get('site')
    apiServer = app.config['API_SERVER_URL']

    if site != None:
        threatsBySiteURI =  '/api/metron/threats/' + site
        assetURI =  '/api/assets/' + site
    try:
        _header = {"X-AUTH-TOKEN": getAuthToken()}
        print(_header)
        response = requests.get(url, headers=_header, params=params)
    except requests.exceptions.RequestException as e:
        error = "Problem occured while accessing threat information. "
        if (e):
            error = error + "Please provide this error code to support: " + str(e)
        return render_template('error.html', error=error)
   
    if (response.status_code != requests.codes.ok):
        error = "Your session has expired or some other issue occured.  Please try to login again."
        return render_template('login.html', error=error)
    
    jData = response.json()
    sites = jData['sites']
    site = request.args.get('site')

    if request.method == 'GET' and site != None:
        authToken = getAuthToken()
        return render_template('threatsbysite.html', username=GUI_MAN.get_user_name(), sites=sites, selectedSite=site,
                               apiServer=apiServer, authToken=authToken, threatsBySiteURI=threatsBySiteURI, assetURI=assetURI)
    return render_template('threatsbysite.html', sites=sites)

# Get the Auth Token from the Cookie
def getAuthToken():
    authToken = request.cookies.get('X-AUTH-TOKEN')
    return authToken

@app.route('/dashboard',methods=['GET'])
def dashboard():
    apiServer = app.config['API_SERVER_URL']
    authToken = getAuthToken()
    return render_template('dashboard.html', username=GUI_MAN.get_user_name(), apiServer=apiServer, authToken=authToken)

@app.route('/userprofile',methods=['GET'])
def userprofile():
    apiServer = app.config['API_SERVER_URL']
    authToken = getAuthToken()
    return render_template('user-profile.html', username=GUI_MAN.get_user_name(), apiServer=apiServer, authToken=authToken)

@app.route('/alert-settings',methods=['GET'])
def alert_settings():
    apiServer = app.config['API_SERVER_URL']
    authToken = getAuthToken()
    return render_template('alert-settings.html', username=GUI_MAN.get_user_name(), apiServer=apiServer, authToken=authToken)

@app.route('/agent-settings',methods=['GET'])
def agent_settings():
    apiServer = app.config['API_SERVER_URL']
    authToken = getAuthToken()
    return render_template('agent-settings.html', username=GUI_MAN.get_user_name(), apiServer=apiServer, authToken=authToken)

@app.route('/facial-upload',methods=['GET'])
def facial_paste():
    apiServer = app.config['API_SERVER_URL']
    authToken = getAuthToken()
    return render_template('facial.html', username=GUI_MAN.get_user_name(), apiServer=apiServer,authToken=authToken)

@app.route('/facial-paste',methods=['GET'])
def facial():
    apiServer = app.config['API_SERVER_URL']
    authToken = getAuthToken()
    return render_template('facial-paste.html', username=GUI_MAN.get_user_name(), apiServer=apiServer, authToken=authToken)


if __name__=='__main__':
    app.run(host="0.0.0.0", port=8888, debug=False)
