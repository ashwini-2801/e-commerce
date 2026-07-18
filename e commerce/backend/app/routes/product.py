import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from backend.app.database import db
from backend.app.models.product import Product
from backend.app.models.category import Category
from backend.app.routes.utils import admin_required

product_bp = Blueprint('product', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Categories API
@product_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200

@product_bp.route('/api/categories', methods=['POST'])
@admin_required
def create_category():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    
    if not name:
        return jsonify({'error': 'Category name is required'}), 400
        
    slug = secure_filename(name.lower().replace(' ', '-'))
    
    if Category.query.filter_by(name=name).first() or Category.query.filter_by(slug=slug).first():
        return jsonify({'error': 'Category with this name or slug already exists'}), 400
        
    new_cat = Category(name=name, description=description, slug=slug)
    db.session.add(new_cat)
    db.session.commit()
    
    return jsonify(new_cat.to_dict()), 201


# Products API
@product_bp.route('/api/products', methods=['GET'])
def get_products():
    query = Product.query
    
    # Filters
    search_q = request.args.get('q', '').strip()
    category_id = request.args.get('category', '')
    sort_by = request.args.get('sort', '')
    
    if search_q:
        query = query.filter(
            (Product.name.ilike(f'%{search_q}%')) | 
            (Product.description.ilike(f'%{search_q}%'))
        )
        
    if category_id:
        try:
            # check if it is integer or slug
            if category_id.isdigit():
                query = query.filter(Product.category_id == int(category_id))
            else:
                cat = Category.query.filter_by(slug=category_id).first()
                if cat:
                    query = query.filter(Product.category_id == cat.id)
        except ValueError:
            pass
            
    # Sorting
    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:
        query = query.order_by(Product.id.asc())
        
    products = query.all()
    return jsonify([p.to_dict() for p in products]), 200

@product_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200

@product_bp.route('/api/products', methods=['POST'])
@admin_required
def add_product():
    # Since we are uploading an image, request is multipart/form-data
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    price_str = request.form.get('price', '0')
    stock_str = request.form.get('stock', '0')
    category_id_str = request.form.get('category_id', '')
    
    if not name or not price_str or not category_id_str:
        return jsonify({'error': 'Name, price, and category_id are required fields'}), 400
        
    try:
        price = float(price_str)
        if price <= 0:
            return jsonify({'error': 'Price must be positive'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid price format'}), 400
        
    try:
        stock = int(stock_str)
        if stock < 0:
            return jsonify({'error': 'Stock cannot be negative'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid stock format'}), 400
        
    try:
        category_id = int(category_id_str)
        if not Category.query.get(category_id):
            return jsonify({'error': 'Invalid category ID'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid category ID format'}), 400
        
    # Image upload
    image_file = request.files.get('image')
    image_url = '/static/uploads/placeholder.webp'  # default placeholder
    
    if image_file and image_file.filename != '':
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            # Add timestamp or product name identifier to avoid conflicts
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            
            # Make sure folder exists
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(filepath)
            image_url = f'/static/uploads/{unique_filename}'
        else:
            return jsonify({'error': 'Invalid image format. Allowed: png, jpg, jpeg, gif, webp'}), 400

    try:
        new_prod = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            image_url=image_url
        )
        db.session.add(new_prod)
        db.session.commit()
        return jsonify(new_prod.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@product_bp.route('/api/products/<int:product_id>', methods=['PUT'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Supports multipart/form-data
    name = request.form.get('name', product.name).strip()
    description = request.form.get('description', product.description).strip()
    price_str = request.form.get('price')
    stock_str = request.form.get('stock')
    category_id_str = request.form.get('category_id')
    
    if not name:
        return jsonify({'error': 'Name is required'}), 400
        
    if price_str is not None:
        try:
            price = float(price_str)
            if price <= 0:
                return jsonify({'error': 'Price must be positive'}), 400
            product.price = price
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400
            
    if stock_str is not None:
        try:
            stock = int(stock_str)
            if stock < 0:
                return jsonify({'error': 'Stock cannot be negative'}), 400
            product.stock = stock
        except ValueError:
            return jsonify({'error': 'Invalid stock format'}), 400
            
    if category_id_str is not None:
        try:
            category_id = int(category_id_str)
            if not Category.query.get(category_id):
                return jsonify({'error': 'Invalid category ID'}), 400
            product.category_id = category_id
        except ValueError:
            return jsonify({'error': 'Invalid category ID format'}), 400

    product.name = name
    product.description = description

    # Image upload
    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        if allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            import time
            unique_filename = f"{int(time.time())}_{filename}"
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(filepath)
            
            # Optionally delete old image if it is not placeholder
            if product.image_url and 'placeholder.webp' not in product.image_url:
                old_path = os.path.join(current_app.config['BASE_DIR'], product.image_url.lstrip('/'))
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass
                        
            product.image_url = f'/static/uploads/{unique_filename}'
        else:
            return jsonify({'error': 'Invalid image format. Allowed: png, jpg, jpeg, gif, webp'}), 400

    try:
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@product_bp.route('/api/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Optionally delete image file
    if product.image_url and 'placeholder.webp' not in product.image_url:
        filepath = os.path.join(current_app.config['BASE_DIR'], product.image_url.lstrip('/'))
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
                
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
