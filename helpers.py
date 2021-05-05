from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(permission: [str]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            permissions = [permission] if (type(permission) is str) else permission
            print(permissions)
            print(current_user.profile)
            if not current_user.is_authenticated:
                abort(403)
            if current_user.profile not in permissions:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_not_allowed(permission: [str]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            permissions = [permission] if (type(permission) is str) else permission
            print(permissions)
            print(current_user.profile)
            if not current_user.is_authenticated:
                abort(403)
            if current_user.profile in permissions:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator