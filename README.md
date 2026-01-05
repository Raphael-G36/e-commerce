# E-Commerce Site with SQLAlchemy

A modern e-commerce website built with Flask and SQLAlchemy.

## Features

- **Database-driven products** using SQLAlchemy
- **Product management** with categories, pricing, stock, and featured products
- **Dynamic product listing** with category filtering
- **Product detail pages** with descriptions and stock information
- **Shopping cart** functionality (client-side)
- **Responsive design** for all devices

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database:**
   The database will be automatically created and seeded when you first run the app. Alternatively, you can run:
   ```bash
   python init_db.py
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the site:**
   Open your browser and go to `http://localhost:5000`

## Database

- **Database file:** `ecommerce.db` (SQLite)
- **Model:** `Product` (defined in `models.py`)
- **Initial data:** 10 sample products are automatically seeded on first run

## Project Structure

```
e-commerce/
├── app.py              # Main Flask application
├── models.py           # SQLAlchemy models
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── templates/          # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── products.html
│   ├── product_detail.html
│   ├── cart.html
│   └── contact.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── ecommerce.db        # SQLite database (created automatically)
```

## Adding Products

You can add products programmatically or through the database:

```python
from app import app
from models import db, Product

with app.app_context():
    new_product = Product(
        name='New Product',
        description='Product description',
        category='Electronics',
        price=99.99,
        image='https://example.com/image.jpg',
        stock=50,
        featured=True
    )
    db.session.add(new_product)
    db.session.commit()
```

## Routes

- `/` - Homepage with featured products
- `/products` - All products (with optional `?category=CategoryName` filter)
- `/product/<id>` - Product detail page
- `/cart` - Shopping cart
- `/contact` - Contact page


