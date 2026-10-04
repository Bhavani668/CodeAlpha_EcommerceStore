# CodeAlpha Simple E-commerce Store

## Technology
Frontend: HTML, CSS
Backend: Python Django
Database: SQLite

## Features
- Product listing
- Product details
- Shopping cart
- User registration and login
- Checkout
- Order processing
- Order history
- Django admin

## Run in VS Code

```bash
python -m venv venv
```

Windows PowerShell:
```bash
.\venv\Scripts\Activate.ps1
```

Install:
```bash
pip install -r requirements.txt
```

Database:
```bash
python manage.py makemigrations
python manage.py migrate
```

Sample products:
```bash
python manage.py seed_products
```

Run:
```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/
