from flask import abort
from flask_login import current_user
from functools import wraps

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.role == role:
                return abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return wrapper