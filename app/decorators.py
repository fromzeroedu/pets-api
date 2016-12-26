from functools import wraps
from flask import request, jsonify

def app_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-APP-ID') is None:
            return jsonify({}), 403
        app_id = request.headers.get('X-APP-ID')
        app_secret = request.headers.get('X-APP-SECRET')
        print(app_id, app_secret)
        if app_id != "jorge" or app_secret != "mySecret":
            return jsonify({}), 403
        return f(*args, **kwargs)
    return decorated_function
