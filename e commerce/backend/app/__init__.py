import os
from flask import Flask
from backend.app.config import Config
from backend.app.database import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Database
    db.init_app(app)
    
    # Register blueprints
    from backend.app.routes.auth import auth_bp
    from backend.app.routes.product import product_bp
    from backend.app.routes.cart import cart_bp
    from backend.app.routes.order import order_bp
    from backend.app.routes.admin import admin_bp
    from backend.app.routes.views import views_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(views_bp) # Page serving views
    
    # Ensure static uploads folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Database table creation and seed data execution
    with app.app_context():
        db.create_all()
        
        # Run database seeding programmatically
        from backend.app.seed import seed_database
        try:
            seed_database()
        except Exception as e:
            app.logger.error(f"Error seeding database: {str(e)}")
            
    return app
