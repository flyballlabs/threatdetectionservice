from flask import Flask, render_template, request, jsonify, make_response 
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True

# Configurations
app.config.from_object('config')

print("API Server:" + app.config['API_SERVER_URL'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = 'http://localhost:7777/api/auth/' + username + "/" + password
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            error = "Make sure the API Server is started and then try to login again"
            return render_template('login.html',error=error);
        jData = response.json()
        if jData['authentication'] == True:
            resp = make_response(render_template('dashboard.html',username=username)); 
            resp.set_cookie('X-AUTH-TOKEN',jData['X-AUTH-TOKEN']);
            return resp;
        else:
            error = "Username or Password was not correct"

    return render_template('login.html',error=error)


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(render_template('login.html'))
    resp.set_cookie('X-AUTH-TOKEN', '', expires=0)
    return resp	 

@app.route('/threats', methods=['GET'])
def threats():
    company = "Flyball-Labs"
    # Grab the sites for the company
    url =  app.config['API_SERVER_URL'] + '/api/company/' + company + "/sites"
    params = request.args.items()
    site = request.args.get('site')
    apiServer = app.config['API_SERVER_URL']
    if site != None:

        threatsBySiteURI =  '/api/metron/threats/' + site
        assetURI =  '/api/assets/' + site
    try:
        _header = getAuthToken()
        response = requests.get(url,headers=_header)
    except requests.exceptions.RequestException as e:
        error = "Problem occured while accessing threat information. "
        if (e):
            error = error + "Please provide this error code to support: " + str(e)
        return render_template('error.html',error=error)
   
    if (response.status_code != requests.codes.ok):
        error = "Your session has expired or some other issue occured.  Please try to login again."
        return render_template('login.html',error=error) 
    
    jData = response.json()
    sites = jData['sites']
    site = request.args.get('site')
    if request.method == 'GET' and site != None:
        return render_template('threatsbysite.html',sites=sites,selectedSite=site,apiServer=apiServer,threatsBySiteURI=threatsBySiteURI,assetURI=assetURI)
    
    return render_template('threatsbysite.html',sites=sites)

# Get the Auth Token from the Cookie 
def getAuthToken():
    authToken = request.cookies.get('X-AUTH-TOKEN')
    header = {'X-AUTH-TOKEN':'%s' % authToken}
    return header;

@app.route('/userprofile',methods=['GET'])
def userprofile():
    return render_template('userprofile.html')

if __name__=='__main__':
    app.run(
       host = "0.0.0.0",
       port = 8888
    )
