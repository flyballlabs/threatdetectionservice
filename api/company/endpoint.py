from flask_restful import Resource

class manageCompany(Resource):
    def post(self):
        try:
           pass
        except Exception as e:
            return {'error': str(e)}