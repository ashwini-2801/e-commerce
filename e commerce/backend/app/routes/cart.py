from flask import Blueprint, request, jsonify, session
from backend.app.database import db
from backend.app.models.cart import Cart, CartItem
from backend.app.models.product import Product
from backend.app.routes.utils import login_required

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('', methods=['GET'])
@login_required
def get_cart():
    user_id = session['user_id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart:
        # Create cart if somehow missing
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        
    items = [item.to_dict() for item in cart.items]
    subtotal = sum(item['subtotal'] for item in items)
    
    # Calculate tax/delivery for total display if required (let's keep simple subtotal and total)
    return jsonify({
        'cart_id': cart.id,
        'items': items,
        'subtotal': subtotal,
        'total': subtotal
    }), 200

@cart_bp.route('', methods=['POST'])
@login_required
def add_to_cart():
    user_id = session['user_id']
    data = request.get_json() or {}
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
        
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than zero'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity value'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
        
    if product.stock <= 0:
        return jsonify({'error': 'Product is out of stock'}), 400

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    
    if cart_item:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            return jsonify({'error': f'Cannot add item. Requested quantity ({new_quantity}) exceeds available stock ({product.stock}).'}), 400
        cart_item.quantity = new_quantity
    else:
        if quantity > product.stock:
            return jsonify({'error': f'Cannot add item. Requested quantity ({quantity}) exceeds available stock ({product.stock}).'}), 400
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        
    try:
        db.session.commit()
        return jsonify({'message': 'Product added to cart', 'item': cart_item.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@cart_bp.route('/<int:product_id>', methods=['PUT'])
@login_required
def update_quantity(product_id):
    user_id = session['user_id']
    data = request.get_json() or {}
    quantity = data.get('quantity')
    
    if quantity is None:
        return jsonify({'error': 'Quantity is required'}), 400
        
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than zero'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid quantity format'}), 400

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
        
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'error': 'Item not found in cart'}), 404
        
    product = Product.query.get(product_id)
    if quantity > product.stock:
        return jsonify({'error': f'Requested quantity ({quantity}) exceeds available stock ({product.stock}).'}), 400
        
    cart_item.quantity = quantity
    
    try:
        db.session.commit()
        return jsonify({'message': 'Cart updated successfully', 'item': cart_item.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@cart_bp.route('/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    user_id = session['user_id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
        
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({'error': 'Item not found in cart'}), 404
        
    try:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@cart_bp.route('', methods=['DELETE'])
@login_required
def clear_cart():
    user_id = session['user_id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
        
    try:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        return jsonify({'message': 'Cart cleared successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
