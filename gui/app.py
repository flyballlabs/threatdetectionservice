from flask import Flask, render_template, request, jsonify 
import requests
import json

app = Flask(__name__)
app.config['DEBUG'] = True

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
            return render_template('dashboard.html',username=username)
        else:
            error = "Username or Password was not correct"

    return render_template('login.html',error=error)

@app.route('/threats', methods=['GET'])
def threats():
    company = "Flyball-Labs"
    # Grab the sites for the company
    url = 'http://10.10.10.97:7777/api/company/' + company + "/sites"
    params = request.args.items()
    site = request.args.get('site')
    apiServer = 'http://10.10.10.97:7777'
    if site != None:

        threatsBySiteURI =  '/api/metron/threats/' + site
        assetURI =  '/api/assets/' + site
    
    response = requests.get(url)
    jData = response.json()
    sites = jData['sites']
    site = request.args.get('site')
    if request.method == 'GET' and site != None:
        return render_template('threatsbysite.html',sites=sites,selectedSite=site,apiServer=apiServer,threatsBySiteURI=threatsBySiteURI,assetURI=assetURI)
    
    return render_template('threatsbysite.html',sites=sites)

@app.route('/userprofile',methods=['GET'])
def userprofile():
    return render_template('userprofile.html')

if __name__=='__main__':
    app.run(
       host = "0.0.0.0",
       port = 8888
    )
