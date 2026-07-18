# ✦ AuraShop - Premium Full-Stack E-Commerce Web Application

AuraShop is a modern, responsive, production-quality Full-Stack E-Commerce web application. It is engineered with a clean Model-View-Controller (MVC) architecture, featuring a modular Python Flask backend, robust database modeling via SQLAlchemy, and a highly polished dark-mode user interface powered by  CSS and JS.
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
