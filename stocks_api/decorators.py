from typing import Callable
from functools import wraps
from flask import request, g


def error_response(message): return ({'error': message}, 401)


def api_key_required(validate_key_func: Callable):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return error_response('API key is required into Authorization header')
            splitted_header = auth_header.split()
            if len(splitted_header) < 2 or splitted_header[0].lower() != 'token':
                return error_response('Invalid Authorization header, correct format is: Token $API_KEY')
            api_key = splitted_header[1]
            is_api_key_valid = validate_key_func(api_key)
            if not is_api_key_valid:
                return error_response('Invalid API key')
            request.api_key = api_key
            return f(*args, **kwargs)
        return wrap
    return decorator
