from functools import wraps
from flask import session, jsonify, request
from backend.app.models.user import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required. Please log in.'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required. Please log in.'}), 401
        if session.get('role') != 'admin':
            return jsonify({'error': 'Forbidden. Administrator privileges required.'}), 403
        return f(*args, **kwargs)
    return decorated_function
