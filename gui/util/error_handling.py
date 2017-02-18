import os
from flask import current_app, abort, request, url_for
from werkzeug.exceptions import HTTPException

def get_redirect_url():
    ''' redirection utility: returns previous url or defaults to index '''
    return request.args.get('next') or request.referrer or url_for('index')

# TODO: add error handling
def url_to_template(URL):
    ''' Takes a url and converts into template name by searching for route keywords in url
        Returns a template name able to render in view, otherwise returns int: -1      '''
    route = URL.split("/")[-1]
    print("Endpoint Route: {}".format(route))
    app = current_app._get_current_object() # dynamically get app object
    with app.app_context(): # bind to app context
        template_dir = app.template_folder
    dir_path = os.path.abspath(os.path.join(os.getcwd(), template_dir))
    print("Template folder path: {}".format(dir_path))
    template_list = os.listdir(dir_path)
    for template in template_list:
        if not str(template).find(route) == -1:
            return str(template)
        elif not str(template).find("-") == -1:
            subs = str(template).split("-")
            for sub in subs:
                print(str(sub))
                if sub == "settings":
                    pass # erroneous use-case
                elif not str(sub).find(route) == -1:
                    return str(template)
    return -1


# custom exceptions:                                                                 #
# provide  boolean redirect param when calling to redirect otherwise -> error.html   #
# redirect param if == True will redirect to redirect url otherwise default == False #

class InvalidLogin(HTTPException):
    ''' Handles login errors that deal with incorrect username or password '''

    def __init__(self, message=None, status_code=None, redirect=False):
        HTTPException.__init__(self)
        self.redirect = redirect
        if message is not None:
            self.message = message
        else:
            self.message = "Username or Password entered is invalid. Call your administrator if you need your password reset"
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 401
        print("in InvalidLogin exception")

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

class BadRequest(HTTPException):
    ''' Handle general http request errors from the view '''

    def __init__(self, message=None, status_code=None, redirect=False):
        HTTPException.__init__(self)
        self.redirect = redirect
        if message is not None:
            self.message = message
        else:
            self.message = "Problem occurred: Bad request"
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 400

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

class Forbidden(HTTPException):
    ''' Handles if user doesn't have permission to the requested resource '''

    def __init__(self, redirect=False):
        HTTPException.__init__(self)
        self.redirect = redirect
        self.code = 403
        self.description = 'You are not authorized to access this resource'

class NotFound(HTTPException):
    ''' Handles requested resources that are not available '''

    def __init__(self, redirect=False):
        HTTPException.__init__(self)
        self.redirect = redirect
        self.code = 404
        self.description = 'Resource was not found, ensure API server is running'

class MethodNotAllowed(HTTPException):
    ''' Handles when unspecified request method is used '''

    def __init__(self, redirect=False):
        HTTPException.__init__(self)
        self.redirect = redirect
        self.code = 405
        self.description = 'The method is not allowed for the requested URL'

class Conflict(HTTPException):
    '''  Handles a request that cannot be completed because it conflicts '''

    def __init__(self, redirect=False):
        HTTPException.__init__(self)
        self.redirect = redirect
        self.code = 409
        self.description = 'A conflict happened while processing the request, ensure input is valid'

class InternalServerError(HTTPException):
    ''' This is a good fallback if an unknown error occurred in the dispatcher '''

    def __init__(self, redirect=False):
        HTTPException.__init__(self)
        self.redirect = redirect
        self.code = 500
        self.description = 'An unexpected error occurred on the server'

# Customize mappings of error handlers for abort() #
# abort.mapping.update({
#     400: BadRequest,
#     401: InvalidLogin,
#     403: Forbidden,
#     404: NotFound,
#     405: MethodNotAllowed,
#     409: Conflict,
#     500: InternalServerError
# })


# TODO: build routines for logging on exceptions
# add this to exceptions for backtrace info propagation
# exc_info = sys.exc_info()

# getting request info from context
#     with self.request_context(request.environ):
#         try:
#             response = self.full_dispatch_request()
#         except Exception as e:
#             response = self.make_response(self.handle_exception(e))
#         return response(environ, start_response)