# ✦ AuraShop - Premium Full-Stack E-Commerce Web Application

AuraShop is a modern, responsive, production-quality Full-Stack E-Commerce web application. It is engineered with a clean Model-View-Controller (MVC) architecture, featuring a modular Python Flask backend, robust database modeling via SQLAlchemy, and a highly polished dark-mode user interface powered by Vanilla CSS and JS.

---

## 🚀 Key Features

### 1. User & Admin Authentication
* Secure profile creation and access management.
* Session-based state protection with password encryption (Werkzeug default salts).
* **Role-Based Access Control (RBAC):**
  * **User role:** Shop, cart management, checkout with billing parameters, order histories, and real-time status trackers.
  * **Admin role:** Dedicated statistics dashboard, full inventory CRUD metrics, category registries, and platform-wide order status updates.

### 2. Product Catalog & Search
* Dynamic catalog query routes supporting text search, category tags filter, and multiple sorting rules (Price Ascending, Price Descending, Newest additions).
* Individual product detail layouts with availability indicators and stock-level bounds checks.

### 3. Shopping Cart & Billing
* Local session carts synced to SQLite.
* Real-time cart calculations (totals, item aggregates) in header.
* Secure checkout collects billing/delivery details and offers multiple payment options (Cash on Delivery, Demo Card with validation, Demo UPI).

### 4. Admin Command Center
* Multi-graph report dashboard using **Chart.js** (Sales over time, orders by state, product categories distribution).
* Real-time warning cards indicating low-stock items.

---

## 📂 Project Directory Structure

```
e commerce/
  backend/
    app/
      __init__.py         # Flask Application Factory & bootstrapper
      config.py           # Application configurations (DB, Session, Uploads)
      database.py         # SQLAlchemy DB object definition
      seed.py             # Seeding routines and Pillow image generators
      models/             # Database Models (M in MVC)
        user.py
        product.py
        category.py
        cart.py
        order.py
      routes/             # Controller Routing Blueprints (C in MVC)
        auth.py           # Authentication REST API endpoints
        product.py        # Products catalog and categories API
        cart.py           # Cart operations and quantity modifications
        order.py          # Checkout placing and status updates
        admin.py          # Admin metrics and dashboard charts JSON
        views.py          # Page-serving views rendering HTML
        utils.py          # Custom decorators (@admin_required, @login_required)
      static/             # Static Assets
        css/
          styles.css      # Core global stylesheet
          admin.css       # Admin dashboard layouts
        js/
          api.js          # REST Client fetch wrapper
          app.js          # Main app session monitor
          toast.js        # Self-dismissing toast alerts
        uploads/          # Dynamic uploads folder (product pictures)
      templates/          # HTML Layout templates (V in MVC)
        base.html         # Navbar, Footer, and core scripts importer
        home.html         # Landing hero page
        products.html     # Shop grid catalog
        product_details.html # Product profile preview
        cart.html         # Cart checklist
        checkout.html     # Checkout details
        order_confirmation.html # Order invoice receipt
        orders.html       # Track order page
        admin_dashboard.html # Admin dashboard
        admin_products.html  # Inventory manager CRUD
        admin_orders.html    # Platform orders manager
        about.html        # Site details
        contact.html      # Message support
  sql/
    schema.sql            # Raw PostgreSQL/MySQL-ready schema layout
    seed.sql              # Database items insert template
  documentation/
    api_documentation.md  # REST API specs
    installation_guide.md # Installation and deployment guides
  requirements.txt        # Backend dependencies
  run.py                  # Startup entry point
  tests_api.py            # Automated REST integrity tests
```

---

## 🛠️ Quick Start

### 1. Prerequisite Installations
Ensure you have **Python 3.10+** set up. Run from the project root:
```bash
pip install -r requirements.txt
```

### 2. Launch Development Server
```bash
python run.py
```

Open `http://localhost:5000` in your web browser.

> [!NOTE]
> The application will automatically create an `ecommerce.db` SQLite file locally and populate it with sample categories, products, and generated placeholder image assets in `backend/app/static/uploads/`.
> The first account you register through the interface will automatically be assigned the `admin` role for immediate testing of administrative panels! Subsequent profiles will register as `user`.
