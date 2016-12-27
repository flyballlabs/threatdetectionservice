from flask import Flask, render_template, request, jsonify, make_response, url_for, redirect, abort, Markup
import requests #, json
from api.sql.models import *
from datetime import datetime

app = Flask('gui_server')
app.config['DEBUG'] = False

# error handling #
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
@app.route('/registration', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        try:
            username = request.json.get('username')
            password = request.json.get('password')
            if username is None or password is None:
                abort(400)    # missing arguments
            if user_data.query.filter_by(username=username).first() is not None:
                abort(400)    # existing user
            
            user_id = user_data.query().count + 1
            firstname = request.json.get('firstname')
            lastname = request.json.get('lastname')
            email = request.json.get('email')
            company_id = request.json.get('company_id')
            status = request.json.get('status')
            phone_number = request.json.get('phone_number')
            
            
            USER = user_data(user_id=user_id, username=username, firstname=firstname, lastname=lastname, password=password, 
                     email=email, company_id=company_id, status=status, phone_number=phone_number, lastlogin = datetime.datetime.now().tostring(),
                     account_type='1', notification=None)
            user_data.hash_password(password)
            db.session.add(USER)
            db.session.commit()
            
            return (jsonify({'username': USER.username}), 201, {'Location': url_for('get_user', id=USER.id, _external=True)})
        except Exception as e:
            return  {
                        'status': 400,
                        'message':'User creation unsuccessful'
                    }
    else:
        return render_template('user_registration.html')
            

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


@app.route('/datamanagement', methods=['GET'])
def show_UI():
    error = None
    return render_template('data_management.html',error=error)

#### TODO - refactoring of code and adding new tables objects ##### 
@app.route('/datamanagement/tables', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tables_redirect():
    route = request.args.get('route')
    print(route)
    #url = 'http://0.0.0.0:7777/api/user/' + username
    
    #'/api/agent', '/api/agent/<string:_mac_address_>'
    #'/api/picontroller', '/api/picontroller/<string:_mac_address_>'
    #'/api/auth/<string:_username>/<string:_password>'
    #'/api/user', '/api/user/<string:_username_>'
    #'/api/company/<string:_company_name_>'
    #'/api/company', '/api/company/sites', '/api/company/<string:_company_name_>/sites'
    #'/api/notification', '/api/notification/<string:_username_>'
    
    '''if site != None:
        if request.method == 'POST':
            if route == 'notifications':
                return render_template('tables_ui.html',sites=sites,selectedSite=site,apiServer=apiServer,threatsBySiteURI=threatsBySiteURI,assetURI=assetURI)
            return render_template('tables_ui.html',sites=sites)
        
        if request.method == 'POST':
            if route == 'users':
                return render_template('tables_ui.html',sites=sites,selectedSite=site,apiServer=apiServer,threatsBySiteURI=threatsBySiteURI,assetURI=assetURI)
            return render_template('tables_ui.html',sites=sites)
        
        if requet.method == "POST":
            if route == 'companies':
                return render_template('tables_ui.html',sites=sites,selectedSite=site,apiServer=apiServer,threatsBySiteURI=threatsBySiteURI,assetURI=assetURI)
            return render_template('tables_ui.html',sites=sites)   
        
        if request.method == "POST":
                return render_template('tables_ui.html',sites=sites,selectedSite=site,apiServer=apiServer,threatsBySiteURI=threatsBySiteURI,assetURI=assetURI)
            return render_template('tables_ui.html',sites=sites)
        
        else:
            return render_template(('tables_ui.html'))
    else:'''    
    
    try:#### TODO getting routing issues only when passing table data ### 
        ### load db table into html table as an example ###
        if route == "notifications":
            table = notification_table(notification_data.query.all())
            return render_template('tables_ui.html',table=table) 
        
        elif route == "users":
            curr_session = db.session
            data = user_data.query.all()
            print(data)
            table = user_table(data)
            print(table.__html__())
            render_template('tables_ui.html',table=table)
            
        elif route == "companies":
            data = company_data.query.all()
            print(data)
            table = company_table(data)
            print(table.__html__())
            render_template('tables_ui.html',table=Markup(table.__html__()))
            
        elif route == "assets":
            table = asset_table(asset_data.query.all())
            render_template('tables_ui.html',table=table)
            
        elif route == "databases":
            
            render_template('tables_ui.html',table=table)
            
        else:
            return {'error': 'Route not available or does not exist'}, 404
        
    except Exception as e:
        return {"An Error Occurred" : e.traceback()}, 404
                
        '''
        if request.method == 'GET':
        if request.method == 'POST':
        if request.method == 'PATCH':
        if request.method == 'DELETE':
        '''
        '''
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
