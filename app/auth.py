"""
Taken from http://flask.pocoo.org/snippets/8/
"""
from app.config import CONFIG

from functools import wraps
from flask import request, Response

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return (not CONFIG.auth_enabled or
        (username == CONFIG.auth['USERNAME'] and
         password == CONFIG.auth['PASSWORD']))

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if CONFIG.auth_enabled:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
        return f(*args, **kwargs)
    return decorated
