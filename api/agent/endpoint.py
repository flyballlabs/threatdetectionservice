from flask_restful import Resource
import time, datetime

## migrate to mysql database ##
data = {
    'id': {
        'glazer': {
            'start': '08:00:00',
            'end': '16:00:00',
            'cmd': '' #'start', 'stop', 'now'
        },
        'loving': {
            'start': '08:00:00',
            'end': '16:00:00',
            'cmd': ''
        },
        'school3': {
            'start': '08:00:00',
            'end': '16:00:00',
            'cmd': ''
        }
    }
}


class timeSync(Resource):
    def get(self):
        dtz = timezone(-timedelta(hours=4))
        dtUTC = datetime.now(dtz)
        dtfUTC = datetime.strftime(dtUTC, '%Y-%m-%d %H:%M:%S')
        return dtfUTC

class piController(Resource):
    def get(self, id):
        #if id in data['id']:
        return {'start': data['id'][id]['start'],'end': data['id'][id]['end'],'cmd': data['id'][id]['cmd']}
    
class update(Resource):
    def post(self, id, start, end, cmd):
        data['id'][id]['start'] = start
        data['id'][id]['end'] = end
        data['id'][id]['cmd'] = cmd
        return 'UPDATED VALUES For:' + id + os.linesep + 'START:' + start + os.linesep + 'END:' + end + os.linesep + 'CMD:' + cmd

## TODO ##
class manageAgents(Resource):
    def post(self):
        try:
           pass
        except Exception as e:
            return {'error': str(e)}