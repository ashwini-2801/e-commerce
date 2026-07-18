from flask import Blueprint, render_template, session, redirect, url_for, request

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
    return render_template('home.html')

@views_bp.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('views.home'))
    return render_template('login.html')

@views_bp.route('/register')
def register():
    if 'user_id' in session:
        return redirect(url_for('views.home'))
    return render_template('register.html')

@views_bp.route('/products')
def products():
    return render_template('products.html')

@views_bp.route('/products/<int:product_id>')
def product_details(product_id):
    return render_template('product_details.html', product_id=product_id)

@views_bp.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('views.login', next=request.path))
    return render_template('cart.html')

@views_bp.route('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('views.login', next=request.path))
    return render_template('checkout.html')

@views_bp.route('/order-confirmation')
def order_confirmation():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))
    order_id = request.args.get('order_id', '')
    return render_template('order_confirmation.html', order_id=order_id)

@views_bp.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('views.login', next=request.path))
    return render_template('orders.html')

@views_bp.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('views.login'))
    return render_template('admin_dashboard.html')

@views_bp.route('/admin/products')
def admin_products():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('views.login'))
    return render_template('admin_products.html')

@views_bp.route('/admin/orders')
def admin_orders():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('views.login'))
    return render_template('admin_orders.html')

@views_bp.route('/about')
def about():
    return render_template('about.html')

@views_bp.route('/contact')
def contact():
    return render_template('contact.html')
