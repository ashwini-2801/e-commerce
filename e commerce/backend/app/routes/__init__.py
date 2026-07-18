from backend.app.routes.auth import auth_bp
from backend.app.routes.product import product_bp
from backend.app.routes.cart import cart_bp
from backend.app.routes.order import order_bp
from backend.app.routes.admin import admin_bp
from backend.app.routes.views import views_bp

__all__ = ['auth_bp', 'product_bp', 'cart_bp', 'order_bp', 'admin_bp', 'views_bp']
