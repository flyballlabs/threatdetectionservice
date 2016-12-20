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
        url = 'http://localhost:6668/api/auth/' + username + "/" + password
        response = requests.get(url)
        jData = response.json()
        if jData['authentication'] == True:
            return render_template('home.html',username=username)
        else:
            error = "Username or Password was not correct"

    return render_template('login.html',error=error)

@app.route('/threats', methods=['GET'])
def threats():
    site = request.args.get('site')
    if request.method == 'GET' and site != None:
        return render_template('threatsbysite.html',site=site)
    
    return render_template('threatsbysite.html',site=site)


if __name__=='__main__':
    app.run(
       host = "0.0.0.0",
       port = 8888
    )
