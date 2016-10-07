# -*- coding: UTF-8 -*-
"""
app1.py: First Python-Flask webapp
"""
from flask import Flask, render_template, jsonify, request  
from cupshelpers.cupshelpers import Device
app = Flask(__name__)    # Construct an instance of Flask class
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/picontroller', methods=['POST', 'GET'])  
def get_picontroller():
    device =request.args.get('device')
       
    if device != "":
        return jsonify({'device': device})  
         

if __name__ == '__main__':  # Script executed directly
    app.run()  # Launch built-in web server and run this Flask webapp
