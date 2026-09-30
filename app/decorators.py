from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role not in roles:
                return redirect(url_for('main.dashboard'))
            return view(*args, **kwargs)
        return wrapped
    return decorator
