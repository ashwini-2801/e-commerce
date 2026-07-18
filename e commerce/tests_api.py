import unittest
import json
from backend.app import create_app, db
from backend.app.models.user import User
from backend.app.models.product import Product
from backend.app.models.category import Category
from backend.app.models.cart import Cart, CartItem
from backend.app.models.order import Order, OrderItem

class AuraShopAPITestCase(unittest.TestCase):
    def setUp(self):
        # Create app instance configured for testing
        self.app = create_app()
        self.app.config.update({
            'TESTING': True,
            # Use separate in-memory database so we do not overwrite main local files
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'testing-secret-key-123'
        })
        self.client = self.app.test_client()
        
        # Open context and create tables
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Clear any auto-seeded data to isolate test cases
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(CartItem).delete()
        db.session.query(Cart).delete()
        db.session.query(Product).delete()
        db.session.query(Category).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Insert a default category for tests
        self.category = Category(name="Test Category", description="Category for testing", slug="test-cat")
        db.session.add(self.category)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 1. Registration tests
    def test_register_success(self):
        payload = {
            'username': 'tester1',
            'email': 'tester1@example.com',
            'password': 'password123',
            'phone': '9876543210'
        }
        res = self.client.post('/api/auth/register', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data['user']['username'], 'tester1')
        self.assertEqual(data['user']['role'], 'admin')  # First registered user becomes admin

    def test_register_invalid_email(self):
        payload = {
            'username': 'tester2',
            'email': 'invalid-email-format',
            'password': 'password123'
        }
        res = self.client.post('/api/auth/register', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertIn('Invalid email format', data['error'])

    def test_register_short_password(self):
        payload = {
            'username': 'tester3',
            'email': 'tester3@example.com',
            'password': '123'
        }
        res = self.client.post('/api/auth/register', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 400)

    # 2. Authentication Login tests
    def test_login_success(self):
        # Pre-register user
        user = User(username='testlogin', email='login@example.com', role='user')
        user.set_password('mysecretpass')
        db.session.add(user)
        db.session.commit()
        
        # Test login
        res = self.client.post('/api/auth/login', data=json.dumps({
            'email': 'login@example.com',
            'password': 'mysecretpass'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['user']['username'], 'testlogin')

    def test_login_fail(self):
        res = self.client.post('/api/auth/login', data=json.dumps({
            'email': 'nonexistent@example.com',
            'password': 'somepassword'
        }), content_type='application/json')
        self.assertEqual(res.status_code, 401)

    # 3. Product Catalog tests
    def test_get_products_empty(self):
        res = self.client.get('/api/products')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data), [])

    def test_add_product_rbac_fail(self):
        # Admin required to add product. Request without logging in.
        res = self.client.post('/api/products', data={
            'name': 'Laptop x1',
            'price': '899.99',
            'category_id': self.category.id
        })
        self.assertEqual(res.status_code, 401)

    # 4. Shopping Cart operations
    def test_cart_operations(self):
        # Register and login user
        self.client.post('/api/auth/register', data=json.dumps({
            'username': 'buyer1',
            'email': 'buyer1@example.com',
            'password': 'password123'
        }), content_type='application/json')
        
        self.client.post('/api/auth/login', data=json.dumps({
            'email': 'buyer1@example.com',
            'password': 'password123'
        }), content_type='application/json')
        
        # Insert a product into DB
        product = Product(name="Smart Watch", price=199.99, stock=5, category_id=self.category.id)
        db.session.add(product)
        db.session.commit()
        
        # Add to cart
        res = self.client.post('/api/cart', data=json.dumps({
            'product_id': product.id,
            'quantity': 2
        }), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        
        # Get cart
        res = self.client.get('/api/cart')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['quantity'], 2)
        self.assertEqual(data['total'], 399.98)

        # Exceed stock limit cart update test
        res = self.client.put(f'/api/cart/{product.id}', data=json.dumps({
            'quantity': 10
        }), content_type='application/json')
        self.assertEqual(res.status_code, 400) # Fails because stock is 5

if __name__ == '__main__':
    unittest.main()
