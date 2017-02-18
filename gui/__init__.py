import os
from flask import Flask, jsonify

# Configurations
from flask import has_request_context
from flask import make_response
from flask import render_template

app = Flask(__name__)
app.config.from_object('config')

# DEBUG: show path app is initialized at
# app.root_path = os.path.join(app.instance_path, '..')
# print("root path: {}\ninstance path: {}".format(app.root_path, app.instance_path))

# import after app object created #
from gui.util.error_handling import *

# TODO: add error handling in exception handlers (master exception_handler) to propagate errors
# custom exception handlers                                                #
# handle exceptions by routing to error page or redirect to previous page  #

@app.errorhandler(BadRequest)
def handle_BadRequest(error):
    msg = error.message
    if error.redirect == False:
        template = 'error.html'
    else:
        URL = get_redirect_url()
        template = url_to_template(URL)

    response = make_response(render_template(template, error=msg))
    response.status_code = error.status_code
    response.headers = {'Content-Type': 'text/html, application/json', 'Accept': 'text/html, application/json'}
    return response

@app.errorhandler(InvalidLogin)
def handle_InvalidLogin(error):
    msg = error.message
    if error.redirect == False:
        template = 'login.html'
    else:
        URL = get_redirect_url()
        template = url_to_template(URL)
    print("in handle_InvalidLogin")

    response = make_response(render_template(template, error=msg))
    response.status_code = error.status_code
    response.headers = {'Content-Type': 'text/html, application/json', 'Accept': 'text/html, application/json'}
    return response

@app.errorhandler(NotFound)
def handle_NotFound(error):
    msg = error.description

    if error.redirect == False:
        template = 'error.html'
    else:
        URL = get_redirect_url()
        template = url_to_template(URL)

    response = make_response(render_template(template, error=msg))
    response.status_code = error.code
    response.headers = {'Content-Type': 'application/json'}
    return response

@app.errorhandler(Forbidden)
def handle_Forbidden(error):
    msg = error.description

    if error.redirect == False:
        template = 'error.html'
    else:
        URL = get_redirect_url()
        template = url_to_template(URL)

    response = make_response(render_template(template, error=msg))
    response.status_code = error.code
    response.headers = {'Content-Type': 'application/json'}
    return response

@app.errorhandler(MethodNotAllowed)
def handle_MethodNotAllowed(error):
    msg = error.description

    if error.redirect == False:
        template = 'error.html'
    else:
        URL = get_redirect_url()
        template = url_to_template(URL)

    response = make_response(render_template(template, error=msg))
    response.status_code = error.code
    response.headers = {'Content-Type': 'application/json'}
    return response

@app.errorhandler(Conflict)
def handle_Conflict(error):
    msg = error.description

    if error.redirect == False:
        template = 'error.html'
    else:
        URL = get_redirect_url()
        template = url_to_template(URL)

    response = make_response(render_template(template, error=msg))
    response.status_code = error.code
    response.headers = {'Content-Type': 'application/json'}
    return response

@app.errorhandler(InternalServerError)
def handle_InternalServerError(error):
    msg = error.description

    if error.redirect == False:
        template = 'error.html'
    else:
        URL = get_redirect_url()
        template = url_to_template(URL)

    response = make_response(render_template(template, error=msg))
    response.status_code = error.code
    response.headers = {'Content-Type': 'application/json'}
    return response

# need to wrap the return expression with headers / token for redirection
# if has_request_context():
#     with app.test_request_context():
#         __headers = request.headers
#         response.headers = __headers
#


# TODO: BUG, register_error_handler() function does not register error handlers properly
# registering error handlers #
# app.register_error_handler(BadRequest, handle_BadRequest)
# app.register_error_handler(InvalidLogin, handle_InvalidLogin)
# app.register_error_handler(NotFound, handle_NotFound)
# app.register_error_handler(Forbidden, handle_Forbidden)
# app.register_error_handler(MethodNotAllowed, handle_MethodNotAllowed)
# app.register_error_handler(InternalServerError, handle_InternalServerError)
# app.register_error_handler(Conflict, handle_Conflict)
