from flask import Flask, render_template, request, jsonify, make_response
from werkzeug.serving import run_simple
import requests, json
from api.rest_server import not_found

app = Flask('gui_server')
app.config['DEBUG'] = False

# error handling #
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# routes #
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = 'http://0.0.0.0:7777/api/auth/' + username + "/" + password
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            error = "Make sure the API Server is started and then try to login again"
            return render_template('login.html',error=error);
        jData = response.json()
        if jData['authentication'] == True:
            return render_template('home.html',username=username)
        else:
            error = "Username or Password was not correct"

    return render_template('login.html',error=error)


@app.route('/threats', methods=['GET'])
def threats():
    company = "Flyball-Labs"
    # Grab the sites for the company
    url = 'http://0.0.0.0:7777/api/company/' + company + "/sites"
    params = request.args.items()
    site = request.args.get('site')
    apiServer = 'http://0.0.0.0:7777'
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


@app.route('/datamanagement', methods=['GET'])
def show_UI():
    error = None
    return render_template('data_management.html',error=error)

#### TODO - refactoring of code and adding new tables objects ##### 
@app.route('/datamanagement/tables', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tables_redirect():
    route = request.args.get('route')
    print(route)
    error = None
    '''
    if route == "notifications":
        pass
    elif route == "users":
        pass
    elif route == "companies":
        pass
    elif route == "assets":
        pass
    elif route == "databases":
        pass
    else:
        return jsonify({'error': 'Route not available or does not exist'}, 404)
        
        if request.method == 'GET':
        if request.method == 'POST':
        if request.method == 'PATCH':
        if request.method == 'DELETE':    
            
            
            username = request.form['username']
            password = request.form['password']
            url = 'http://0.0.0.0:7777/api/auth/' + username + "/" + password
            try:
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                error = "Make sure the API Server is started and then try to login again"
                return render_template('login.html',error=error);
            jData = response.json()
            if jData['authentication'] == True:
                return render_template('home.html',username=username)
            else:
                error = "Username or Password was not correct"
    
        return render_template('tables_ui.html',error=error)
        
        company = "Flyball-Labs"
        # Grab the sites for the company
        url = 'http://0.0.0.0:7777/api/company/' + company + "/sites"
        params = request.args.items()
        site = request.args.get('site')
        apiServer = 'http://0.0.0.0:7777'
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
        '''

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
