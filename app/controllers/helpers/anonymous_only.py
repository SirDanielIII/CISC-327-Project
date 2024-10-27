from flask import abort
from flask_login import current_user
from functools import wraps

def anonymous_only(func):
    @wraps(func)
    def wrapper():
        if current_user.is_authenticated:
                return abort(403)  # Forbidden
        func()
    return wrapper