# AuraShop RESTful API Documentation

This document describes the API contracts, payloads, and response structures for the AuraShop RESTful backend services.

All endpoints return JSON responses and use standard HTTP status codes.

---

## 🔒 1. Authentication APIs

### 1.1 Register User
* **Endpoint:** `/api/auth/register`
* **Method:** `POST`
* **Content-Type:** `application/json`
* **Request Payload:**
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "phone": "9876543210",
    "address": "123 Main Street",
    "city": "Dallas",
    "state": "Texas",
    "pin_code": "75001"
  }
  ```
* **Success Response (201 Created):**
  ```json
  {
    "message": "Registration successful",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "admin",
      "phone": "9876543210",
      "address": "123 Main Street",
      "city": "Dallas",
      "state": "Texas",
      "pin_code": "75001",
      "created_at": "2026-07-18T14:35:10.123456"
    }
  }
  ```

### 1.2 User Login
* **Endpoint:** `/api/auth/login`
* **Method:** `POST`
* **Content-Type:** `application/json`
* **Request Payload:**
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
* **Success Response (200 OK):**
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "username": "johndoe",
      "role": "admin"
    }
  }
  ```

### 1.3 User Logout
* **Endpoint:** `/api/auth/logout`
* **Method:** `POST`
* **Success Response (200 OK):**
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

### 1.4 Get Active Session User
* **Endpoint:** `/api/auth/me`
* **Method:** `GET`
* **Success Response (200 OK - Logged In):**
  ```json
  {
    "logged_in": true,
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "role": "admin"
    }
  }
  ```

---

## 📦 2. Product Catalog APIs

### 2.1 Fetch Categories
* **Endpoint:** `/api/categories`
* **Method:** `GET`
* **Success Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "Electronics",
      "description": "Gadgets, smartphones, and laptops",
      "slug": "electronics"
    }
  ]
  ```

### 2.2 Add Category (Admin Only)
* **Endpoint:** `/api/categories`
* **Method:** `POST`
* **Request Payload:**
  ```json
  {
    "name": "Fitness",
    "description": "Exercise equipment"
  }
  ```

### 2.3 Fetch Products (Filtered & Sorted)
* **Endpoint:** `/api/products`
* **Method:** `GET`
* **Query Parameters:**
  * `q` (Optional) - Text search query (matches name or description).
  * `category` (Optional) - Category ID or category slug to filter items.
  * `sort` (Optional) - Sorting method. Options: `price_asc`, `price_desc`, `newest`.
* **Success Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "Quantum Laptop",
      "description": "Intel i7 processor...",
      "price": 1199.99,
      "stock": 15,
      "category_id": 1,
      "category_name": "Electronics",
      "image_url": "/static/uploads/laptop.webp",
      "created_at": "2026-07-18T14:35:10.123456"
    }
  ]
  ```

### 2.4 Add Product (Admin Only)
* **Endpoint:** `/api/products`
* **Method:** `POST`
* **Content-Type:** `multipart/form-data`
* **Form Parameters:**
  * `name` (Required string)
  * `description` (Optional string)
  * `price` (Required float)
  * `stock` (Required integer)
  * `category_id` (Required integer)
  * `image` (Optional binary file upload)

### 2.5 Edit Product (Admin Only)
* **Endpoint:** `/api/products/<id>`
* **Method:** `PUT`
* **Content-Type:** `multipart/form-data`
* **Form Parameters:** (Any subset of fields to edit, plus optional image)

### 2.6 Delete Product (Admin Only)
* **Endpoint:** `/api/products/<id>`
* **Method:** `DELETE`
* **Success Response (200 OK):**
  ```json
  {
    "message": "Product deleted successfully"
  }
  ```

---

## 🛒 3. Shopping Cart APIs

### 3.1 Get Cart Details
* **Endpoint:** `/api/cart`
* **Method:** `GET`
* **Success Response (200 OK):**
  ```json
  {
    "cart_id": 1,
    "items": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "Quantum Laptop",
        "product_price": 1199.99,
        "product_image": "/static/uploads/laptop.webp",
        "product_stock": 15,
        "quantity": 1,
        "subtotal": 1199.99
      }
    ],
    "subtotal": 1199.99,
    "total": 1199.99
  }
  ```

### 3.2 Add to Cart
* **Endpoint:** `/api/cart`
* **Method:** `POST`
* **Request Payload:**
  ```json
  {
    "product_id": 1,
    "quantity": 2
  }
  ```

### 3.3 Edit Cart Quantity
* **Endpoint:** `/api/cart/<product_id>`
* **Method:** `PUT`
* **Request Payload:**
  ```json
  {
    "quantity": 3
  }
  ```

---

## 🚀 4. Checkout & Order APIs

### 4.1 Place Order (Checkout)
* **Endpoint:** `/api/orders`
* **Method:** `POST`
* **Request Payload:**
  ```json
  {
    "customer_name": "John Doe",
    "mobile_number": "9876543210",
    "delivery_address": "123 Main Street",
    "city": "Dallas",
    "state": "Texas",
    "pin_code": "75001",
    "payment_method": "COD"
  }
  ```
* **Success Response (201 Created):**
  ```json
  {
    "message": "Order placed successfully",
    "order_id": "ORD-20260718-182512-4829",
    "order": {
      "id": "ORD-20260718-182512-4829",
      "customer_name": "John Doe",
      "total_amount": 1199.99,
      "status": "Pending",
      "payment_status": "Pending"
    }
  }
  ```

### 4.2 Get Orders List
* **Endpoint:** `/api/orders`
* **Method:** `GET`
* **Query Parameters:**
  * `all` (Optional, admin only) - set to `true` to fetch all orders system-wide.
* **Success Response (200 OK):** (Array of Order objects)

### 4.3 Update Order Status (Admin / User Cancel)
* **Endpoint:** `/api/orders/<id>`
* **Method:** `PUT`
* **Request Payload:**
  ```json
  {
    "status": "Shipped"
  }
  ```
  *(Note: Users can only change status to "Cancelled" if current status is "Pending" or "Confirmed".)*
