from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.app.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'admin'
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    pin_code = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to cart and orders
    carts = db.relationship('Cart', backref='user', cascade='all, delete-orphan', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'pin_code': self.pin_code,
            'created_at': self.created_at.isoformat()
        }
        if include_sensitive:
            data['password_hash'] = self.password_hash
        return data
