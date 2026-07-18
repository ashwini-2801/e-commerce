# Installation and Setup Guide

This document describes how to deploy, configure, and run the AuraShop E-Commerce application.

---

## 💻 Local Development Setup

### 1. Clone the Codebase
Navigate into your workspace directory where you want to unpack the files.

### 2. Configure Virtual Environment
It is highly recommended to isolate dependencies inside a Python virtual environment:
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Store
Launch the Flask development server:
```bash
python run.py
```
Flask will boot up on port `5000` by default. Browse `http://127.0.0.1:5000` to start testing.

---

## 🗄️ Database Configurations

By default, AuraShop uses **SQLite** (`sqlite:///ecommerce.db`). This requires zero configuration.

### Switching to PostgreSQL (Recommended for Production)
Because we use **SQLAlchemy**, you can switch the backend database engine simply by supplying the `DATABASE_URL` environment parameter.

1. Install a PostgreSQL database server locally or host it on services like Heroku, Supabase, or AWS RDS.
2. Setup database credentials and create a blank database:
   ```sql
   CREATE DATABASE aurashop;
   ```
3. Set the environment variable before launching the server:
   ```powershell
   # Windows PowerShell
   $env:DATABASE_URL="postgresql://username:password@localhost:5432/aurashop"
   
   # Linux / macOS / Git Bash
   export DATABASE_URL="postgresql://username:password@localhost:5432/aurashop"
   ```
4. Start the application (`python run.py`). SQLAlchemy will automatically detect the PostgreSQL connection, migrate the entire schema layout, and seed categories/sample products.

---

## ⚙️ Environment Variables Configs

You can customize runtime variables by configuring environment variables:

| Variable | Description | Default |
| --- | --- | --- |
| `FLASK_ENV` | Application environment state | `development` |
| `SECRET_KEY` | Salt key for cookies and credentials validation | `dev-secret-key-ecommerce-12345` |
| `DATABASE_URL` | SQLAlchemy connection URI string | `sqlite:///ecommerce.db` |
| `PORT` | Listening port for the application | `5000` |

---

## 🔐 Administrative Access Setup

For ease of local evaluation, AuraShop implements a bootstrap trigger:
* **The first account registered via the standard `/register` form will automatically receive the `admin` role.**
* All subsequent registrations will receive the default `user` role.

To reset the database, simply delete the local `ecommerce.db` file and restart Flask.
