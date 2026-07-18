import time
import random
from datetime import datetime
from flask import Blueprint, request, jsonify, session
from backend.app.database import db
from backend.app.models.order import Order, OrderItem
from backend.app.models.cart import Cart, CartItem
from backend.app.models.product import Product
from backend.app.routes.utils import login_required

order_bp = Blueprint('order', __name__, url_prefix='/api/orders')

def generate_order_id():
    # Format: ORD-YYYYMMDD-HHMMSS-RAND4
    now = datetime.now()
    date_str = now.strftime("%Y%m%d-%H%M%S")
    rand_digits = "".join([str(random.randint(0, 9)) for _ in range(4)])
    return f"ORD-{date_str}-{rand_digits}"

@order_bp.route('', methods=['POST'])
@login_required
def checkout():
    user_id = session['user_id']
    data = request.get_json() or {}
    
    customer_name = data.get('customer_name', '').strip()
    mobile_number = data.get('mobile_number', '').strip()
    delivery_address = data.get('delivery_address', '').strip()
    city = data.get('city', '').strip()
    state = data.get('state', '').strip()
    pin_code = data.get('pin_code', '').strip()
    payment_method = data.get('payment_method', '').strip()  # 'COD', 'UPI', 'CARD'
    
    # Validations
    if not all([customer_name, mobile_number, delivery_address, city, state, pin_code, payment_method]):
        return jsonify({'error': 'All checkout fields are required'}), 400
        
    if not mobile_number.isdigit() or len(mobile_number) < 10 or len(mobile_number) > 12:
        return jsonify({'error': 'Invalid mobile number format. Should be 10-12 digits.'}), 400
        
    if len(pin_code) < 5 or len(pin_code) > 8:
        return jsonify({'error': 'Invalid PIN/ZIP code format.'}), 400
        
    if payment_method not in ['COD', 'UPI', 'CARD']:
        return jsonify({'error': 'Invalid payment method selected.'}), 400

    # Fetch User's Cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({'error': 'Your shopping cart is empty.'}), 400
        
    # Start checking items and stock
    order_items_to_create = []
    total_amount = 0
    
    # Transactional check
    for item in cart.items:
        prod = item.product
        if not prod:
            return jsonify({'error': f'Product with ID {item.product_id} no longer exists.'}), 404
            
        if prod.stock < item.quantity:
            return jsonify({
                'error': f'Insufficient stock for product "{prod.name}". '
                         f'Available: {prod.stock}, Cart quantity: {item.quantity}'
            }), 400
            
        total_amount += prod.price * item.quantity
        order_items_to_create.append((prod, item.quantity, prod.price))
        
    # Generate Order ID and create Order
    order_id = generate_order_id()
    
    # For demo card and upi payment options, mark as 'Paid' immediately, for COD mark 'Pending'
    payment_status = 'Paid' if payment_method in ['CARD', 'UPI'] else 'Pending'
    
    try:
        # Create Order
        new_order = Order(
            id=order_id,
            user_id=user_id,
            customer_name=customer_name,
            mobile_number=mobile_number,
            delivery_address=delivery_address,
            city=city,
            state=state,
            pin_code=pin_code,
            payment_method=payment_method,
            payment_status=payment_status,
            total_amount=total_amount,
            status='Pending'
        )
        db.session.add(new_order)
        
        # Create Order Items & Deduct Stock
        for prod, qty, price in order_items_to_create:
            order_item = OrderItem(
                order_id=order_id,
                product_id=prod.id,
                quantity=qty,
                price_at_purchase=price
            )
            db.session.add(order_item)
            
            # Deduct stock
            prod.stock -= qty
            
        # Clear User's Cart Items
        CartItem.query.filter_by(cart_id=cart.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order placed successfully',
            'order_id': order_id,
            'order': new_order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error during checkout: {str(e)}'}), 500

@order_bp.route('', methods=['GET'])
@login_required
def get_orders():
    user_id = session['user_id']
    role = session.get('role')
    
    # If admin requests all, show all orders
    view_all = request.args.get('all', 'false').lower() == 'true'
    
    if view_all and role == 'admin':
        orders = Order.query.order_by(Order.created_at.desc()).all()
    else:
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
    return jsonify([o.to_dict() for o in orders]), 200

@order_bp.route('/<string:order_id>', methods=['GET'])
@login_required
def get_order_details(order_id):
    user_id = session['user_id']
    role = session.get('role')
    
    order = Order.query.get_or_404(order_id)
    
    # Authorize: Only order owner or admin
    if order.user_id != user_id and role != 'admin':
        return jsonify({'error': 'Access denied. You do not own this order.'}), 403
        
    return jsonify(order.to_dict()), 200

@order_bp.route('/<string:order_id>', methods=['PUT'])
@login_required
def update_order(order_id):
    user_id = session['user_id']
    role = session.get('role')
    
    order = Order.query.get_or_404(order_id)
    data = request.get_json() or {}
    new_status = data.get('status', '').strip()
    
    if not new_status:
        return jsonify({'error': 'Status field is required'}), 400
        
    valid_statuses = ['Pending', 'Confirmed', 'Packed', 'Shipped', 'Out for Delivery', 'Delivered', 'Cancelled']
    if new_status not in valid_statuses:
        return jsonify({'error': f'Invalid order status. Must be one of: {", ".join(valid_statuses)}'}), 400

    # Business Rule:
    # 1. Admin can update to any status.
    # 2. User can only cancel (status='Cancelled') their own order, and only if it's currently 'Pending' or 'Confirmed'.
    
    if role != 'admin':
        if order.user_id != user_id:
            return jsonify({'error': 'Access denied.'}), 403
        if new_status != 'Cancelled':
            return jsonify({'error': 'Users can only update status to "Cancelled".'}), 400
        if order.status not in ['Pending', 'Confirmed']:
            return jsonify({'error': f'Cannot cancel order at this stage. Current status: "{order.status}"'}), 400

    old_status = order.status
    order.status = new_status
    
    # If the order is updated to 'Cancelled', return stock back to inventory
    if new_status == 'Cancelled' and old_status != 'Cancelled':
        for item in order.items:
            prod = Product.query.get(item.product_id)
            if prod:
                prod.stock += item.quantity
                
        # Also mark payment status as Failed/Refunded if they paid already
        if order.payment_status == 'Paid' and order.payment_method in ['CARD', 'UPI']:
            order.payment_status = 'Refunded'
            
    # If status changes to Delivered and was COD, mark payment_status as Paid
    if new_status == 'Delivered' and order.payment_method == 'COD':
        order.payment_status = 'Paid'

    try:
        db.session.commit()
        return jsonify({
            'message': f'Order status updated to {new_status} successfully.',
            'order': order.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
