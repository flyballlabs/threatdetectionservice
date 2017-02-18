# API_SERVER_URL: The hostname/ip and port number of the Threat Management Platform API Server
# default value: Your local ip address will be used with the default port number of 7777
# API_SERVER_URL = "http://<your ip>:7777"

# If TRAP_HTTP_EXCEPTIONS is set to True Flask will not execute the error handlers of HTTP exceptions
# but instead treat the exception like any other and bubble it through the exception stack.
TRAP_HTTP_EXCEPTIONS = True

# If TRAP_BAD_REQUEST_ERRORS is set to True you will get a regular traceback from request specific data.
# Normally the requests will raise errors that are bad request exceptions, that help w/ handling but are
# sometimes hard to troubleshoot when other python routines throw the same exception.
TRAP_BAD_REQUEST_ERRORS = True

ERROR_404_HELP = False
# PROPAGATE_EXCEPTIONS = True