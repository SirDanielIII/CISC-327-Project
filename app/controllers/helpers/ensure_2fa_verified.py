from functools import wraps

from flask import flash, redirect, session, request
from flask_login import current_user


def ensure_2fa_verified(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.is_2fa_auth_enabled and not session.get('2fa_verified'):
            flash('2FA Verification is required before accessing this page.', 'error')
            return redirect(f'/verify_2fa?next={request.path}')  # Forbidden
        return func(*args, **kwargs)

    return wrapper
