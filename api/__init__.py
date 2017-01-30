''' 
############# flask / api / cors config ################  
app be defined in the project as a module-level variable
application instantiation for all api-related functions 
'''
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask('rest_server') # defines app object for rest_server to load #
API = Api(app) # defines api object for adding resources #
CORS(app) # adds cross-site protection to app #