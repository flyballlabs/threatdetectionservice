from flask_restful import Resource
from sql.models import *  #import all of the models from models.py

class manageCompany(Resource):
    def post(self):
        try:
           pass
        except Exception as e:
            return {'error': str(e)}