from functools import wraps
from flask import jsonify
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function


def admin_or_worker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (current_user.role != 'admin' and current_user.role != 'worker'):
            return jsonify({"success": False, "message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function