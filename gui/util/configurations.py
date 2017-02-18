from gui import app
from api.util import dynamic

def set_api_url(ip=None, port=None):
    ''' Sets API_SERVER_URL in config file if not already specified
        ip and port are optional params and if provided set config
        returns 0 if no errors, returns -1 if error occurred    '''
    try:
        API_SERVER = ""
        if ('API_SERVER_URL' in app.config) and len(app.config['API_SERVER_URL']) > 0:
            print("API_SERVER_URL already set.")
        elif (ip != None or port != None):
            if (port == None): # ip must be not none
                API_SERVER = "http://{}:7777".format(ip)
            elif (ip == None): # port must be not none
                cur_ip = dynamic.get_current_ip()
                API_SERVER = "http://{}:{}".format(cur_ip, port)
            app.config['API_SERVER_URL'] = API_SERVER
        else: #Assume the the server is located on the local server
            cur_ip = dynamic.get_current_ip()
            API_SERVER = "http://{}:7777".format(cur_ip)
            app.config['API_SERVER_URL'] = API_SERVER
        print("API_SERVER_URL successfully set: {}".format(API_SERVER))
        return 0
    except Exception as e:
        return -1