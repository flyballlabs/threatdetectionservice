# TODO: Define what vars to store here, API_SERVER isn't really sensitive data but username is
class GUI:
    ''' Container for encapsulation / data-hiding of configuration variables.
        Variables that are sensitive but used during operation, load here.
        GUI is created when gui_server.py starts and destroyed on shut down. '''

    def __init__(self, user_name=None, api_server_url=None):
        self.__user_name = user_name
        self.__api_server_url = api_server_url
        print("GUI configuration variables initialized")

    def set_user_name(self, user_name):
        self.__user_name = user_name

    def get_user_name(self):
        return self.__user_name

    def set_api_server_url(self, api_server_url):
        self.__api_server_url = api_server_url

    def get_api_server_url(self):
        return self.__api_server_url

    def __repr__(self):
        if self.__user_name == None or self.__api_server_url == None:
            return "GUI Not Valid"
        return "GUI Valid"

    def __del__(self):
        self.__user_name = ""
        self.__api_server_url = ""
        print("GUI configuration variables destroyed")