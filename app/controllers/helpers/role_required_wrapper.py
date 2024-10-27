from flask import flash, redirect
from flask_login import current_user
from functools import wraps

def role_required(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.account_type == role:
                flash('The requested page requires different permissions to be accessed.','error')
                return redirect('/')  # Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return wrapper