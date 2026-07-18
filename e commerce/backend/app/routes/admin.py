from flask import Blueprint, jsonify, session
from sqlalchemy import func
from backend.app.database import db
from backend.app.models.user import User
from backend.app.models.product import Product
from backend.app.models.order import Order
from backend.app.models.category import Category
from backend.app.routes.utils import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_data():
    try:
        # Total counts
        total_users = User.query.filter_by(role='user').count()
        total_products = Product.query.count()
        total_orders = Order.query.count()
        
        # Calculate revenue (excluding cancelled orders)
        revenue_result = db.session.query(func.sum(Order.total_amount)).filter(Order.status != 'Cancelled').first()
        revenue = revenue_result[0] if revenue_result[0] is not None else 0.0
        
        # Order statuses
        pending_orders = Order.query.filter_by(status='Pending').count()
        delivered_orders = Order.query.filter_by(status='Delivered').count()
        
        # Low stock products (stock < 5)
        low_stock_items = Product.query.filter(Product.stock <= 5).all()
        low_stock_products = [p.to_dict() for p in low_stock_items]
        
        # Recent orders (top 10)
        recent_items = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        recent_orders = [o.to_dict() for o in recent_items]
        
        # Chart Data 1: Sales revenue over time (Grouped by Date, last 7 days)
        # We can extract the date from created_at
        sales_by_date = db.session.query(
            func.date(Order.created_at).label('order_date'),
            func.sum(Order.total_amount).label('daily_total')
        ).filter(Order.status != 'Cancelled')\
         .group_by(func.date(Order.created_at))\
         .order_by(func.date(Order.created_at).desc())\
         .limit(7).all()
         
        # Format sales chart data (chronological order)
        chart_sales = {
            'labels': [str(row.order_date) for row in reversed(sales_by_date)],
            'data': [float(row.daily_total) for row in reversed(sales_by_date)]
        }
        
        # Chart Data 2: Orders distribution by Status
        status_counts = db.session.query(
            Order.status,
            func.count(Order.id)
        ).group_by(Order.status).all()
        
        chart_status = {
            'labels': [row[0] for row in status_counts],
            'data': [row[1] for row in status_counts]
        }
        
        # Chart Data 3: Products distribution by Category
        cat_counts = db.session.query(
            Category.name,
            func.count(Product.id)
        ).join(Product, Category.id == Product.category_id)\
         .group_by(Category.name).all()
         
        chart_categories = {
            'labels': [row[0] for row in cat_counts],
            'data': [row[1] for row in cat_counts]
        }
        
        return jsonify({
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'revenue': round(revenue, 2),
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders,
            'low_stock_products': low_stock_products,
            'recent_orders': recent_orders,
            'charts': {
                'sales': chart_sales,
                'status': chart_status,
                'categories': chart_categories
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to gather admin metrics: {str(e)}'}), 500
