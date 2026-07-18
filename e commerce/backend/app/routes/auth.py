import re
from flask import Blueprint, request, jsonify, session
from backend.app.database import db
from backend.app.models.user import User
from backend.app.models.cart import Cart

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Helper: Validations
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone) is not None if phone else True

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    phone = data.get('phone', '').strip()
    address = data.get('address', '').strip()
    city = data.get('city', '').strip()
    state = data.get('state', '').strip()
    pin_code = data.get('pin_code', '').strip()
    
    # Validations
    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required fields'}), 400
        
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long'}), 400
        
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
        
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
    if phone and not is_valid_phone(phone):
        return jsonify({'error': 'Phone number must be exactly 10 digits'}), 400

    # Check uniqueness
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username is already taken'}), 400
        
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email is already registered'}), 400

    # Determine role: First user is admin (for ease of testing), subsequent are users
    is_first_user = User.query.first() is None
    role = 'admin' if is_first_user else 'user'

    try:
        new_user = User(
            username=username,
            email=email,
            role=role,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pin_code=pin_code
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Initialize an empty cart for this user
        new_cart = Cart(user_id=new_user.id)
        db.session.add(new_cart)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
        
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
        
    # Create session
    session['user_id'] = user.id
    session['role'] = user.role
    session['username'] = user.username
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'logged_in': False}), 200
        
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'logged_in': False}), 200
        
    return jsonify({
        'logged_in': True,
        'user': user.to_dict()
    }), 200
