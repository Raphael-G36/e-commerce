# E-Commerce Site (Flask + SQLAlchemy)

Lightweight e-commerce demo built with Flask and SQLAlchemy.

## Features

- Database-driven products using SQLAlchemy
- Product management with categories, pricing, stock, and featured products
- Dynamic product listing with category filtering
- Product detail pages with descriptions and stock information
- Shopping cart (client-side) and responsive design

## Quick setup & run

1) Create a virtual environment (recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

macOS / Linux / Git Bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Initialize the database (optional — app may auto-create on first run)

```bash
python init_db.py
```

4) Run the app

```bash
python app.py
```

Open http://localhost:5000 in your browser.

### Notes
- To use `flask run`, set `FLASK_APP=app.py` and `FLASK_ENV=development` (or use environment variables on Windows).
- Store secrets and environment variables in a local `.env` file (already ignored by `.gitignore`).

## Database

- Default: SQLite file in project root (e.g., `ecommerce.db`).
- Models are defined in `models.py`. Use `init_db.py` to (re)create and seed the database.

## Project structure

Top-level files and folders you will care about:

- `app.py` — main Flask application and routes
- `models.py` — SQLAlchemy models and DB setup
- `init_db.py` — helper to create and seed the DB
- `requirements.txt` — Python dependencies
- `static/` — CSS and JS
- `templates/` — Jinja2 HTML templates

Example tree (partial):

```
e-commerce/
├── app.py
├── models.py
├── init_db.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── products.html
    └── product_detail.html
```

## Adding products (example)

You can add products programmatically from a Python REPL or script:

```python
from app import app
from models import db, Product

with app.app_context():
    p = Product(
        name='New Product',
        description='Description',
        category='Category',
        price=9.99,
        image='',
        stock=10,
        featured=False
    )
    db.session.add(p)
    db.session.commit()
```

## Routes (common)

- `/` — Homepage (featured products)
- `/products` — Product listings (optional `?category=` filter)
- `/product/<id>` — Product detail
- `/cart` — Shopping cart
- `/contact` — Contact page

## Common tasks

- Re-seed DB: `python init_db.py`
- Update product prices: `python update_prices.py`

## Development tips

- Use a dedicated virtual environment (`.venv`) per project.
- The `.gitignore` already ignores local envs, IDE settings, and secrets.
- For deployment, consider switching from SQLite to Postgres/MySQL and configuring connection in `app.py`/`models.py`.

---

If you want, I can also:

- add a `Dockerfile` and `docker-compose.yml` for local development;
- add simple GitHub Actions CI for linting and tests;
- commit these changes to git.

If you'd like one of those, tell me which and I'll add it.
```

macOS / Linux / Git Bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Initialize the database (optional — app may auto-create on first run)

```bash
python init_db.py
```

4) Run the app

```bash
python app.py
```

Open http://localhost:5000 in your browser.

### Notes
- To use `flask run`, set `FLASK_APP=app.py` and `FLASK_ENV=development` (or use environment variables on Windows).
- Store secrets and environment variables in a local `.env` file (already ignored by `.gitignore`).

## Database

- Default: SQLite file in project root (e.g., `ecommerce.db`).
- Models are defined in `models.py`. Use `init_db.py` to (re)create and seed the database.

## Project structure

Top-level files and folders you will care about:

- `app.py` — main Flask application and routes
- `models.py` — SQLAlchemy models and DB setup
- `init_db.py` — helper to create and seed the DB
- `requirements.txt` — Python dependencies
- `static/` — CSS and JS
- `templates/` — Jinja2 HTML templates

Example tree (partial):

```
e-commerce/
├── app.py
├── models.py
├── init_db.py
├── requirements.txt
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    ├── base.html
    ├── index.html
    ├── products.html
    └── product_detail.html
```

## Adding products (example)

You can add products programmatically from a Python REPL or script:

```python
from app import app
from models import db, Product

with app.app_context():
    p = Product(
        name='New Product',
        description='Description',
        category='Category',
        price=9.99,
        image='',
        stock=10,
        featured=False
    )
    db.session.add(p)
    db.session.commit()
```

## Routes (common)

- `/` — Homepage (featured products)
- `/products` — Product listings (optional `?category=` filter)
- `/product/<id>` — Product detail
- `/cart` — Shopping cart
- `/contact` — Contact page

## Common tasks

- Re-seed DB: `python init_db.py`
- Update product prices: `python update_prices.py`

## Development tips

- Use a dedicated virtual environment (`.venv`) per project.
- The `.gitignore` already ignores local envs, IDE settings, and secrets.
- For deployment, consider switching from SQLite to Postgres/MySQL and configuring connection in `app.py`/`models.py`.

---

If you want, I can also:

- add a `Dockerfile` and `docker-compose.yml` for local development;
- add simple GitHub Actions CI for linting and tests;
- commit these changes to git.

If you'd like one of those, tell me which and I'll add it.
# E-Commerce Site (Flask + SQLAlchemy)

Lightweight e-commerce demo built with Flask and SQLAlchemy.

## Quick setup & run

1) Create a virtual environment (recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

macOS / Linux / Git Bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Initialize the database (optional — app may auto-create on first run)

```bash
python init_db.py
```

4) Run the app

```bash
python app.py
```

Open http://localhost:5000 in your browser.

### Notes
- If you prefer `flask run`, set `FLASK_APP=app.py` and `FLASK_ENV=development`.
- Put environment variables and secrets in a local `.env` file (this project ignores `.env`).

### Project layout (important files)

- `app.py` — Flask application entry
- `models.py` — SQLAlchemy models and DB setup
- `init_db.py` — helper to (re)create and seed the DB
- `requirements.txt` — Python dependencies
- `templates/` and `static/` — frontend assets and templates

### Common tasks
- Re-seed DB: `python init_db.py`
- Update product prices script: `python update_prices.py`

### Development tips
- Use a virtual environment per project to avoid global package conflicts.
- The repository `.gitignore` excludes local envs, IDE settings, and secrets.

Need anything else (deploy steps, Dockerfile, CI)? Open an issue or ask here.

# E-Commerce Site (Flask + SQLAlchemy)

Lightweight e-commerce demo built with Flask and SQLAlchemy.

## Quick setup & run

1) Create a virtual environment (recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

macOS / Linux / Git Bash:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Initialize the database (optional — app may auto-create on first run)

```bash
python init_db.py
```

4) Run the app

```bash
python app.py
```

Open http://localhost:5000 in your browser.

### Notes
- If you prefer `flask run`, set `FLASK_APP=app.py` and `FLASK_ENV=development`.
- Put environment variables and secrets in a local `.env` file (this project ignores `.env`).

### Project layout (important files)

- `app.py` — Flask application entry
- `models.py` — SQLAlchemy models and DB setup
- `init_db.py` — helper to (re)create and seed the DB
- `requirements.txt` — Python dependencies
- `templates/` and `static/` — frontend assets and templates

### Common tasks
- Re-seed DB: `python init_db.py`
- Update product prices script: `python update_prices.py`

### Development tips
- Use a virtual environment per project to avoid global package conflicts.
- The repository `.gitignore` excludes local envs, IDE settings, and secrets.

Need anything else (deploy steps, Dockerfile, CI)? Open an issue or ask here.

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Initialize the database (optional — app may auto-create on first run)

```bash
python init_db.py
```

4) Run the app

```bash
python app.py
```

Open http://localhost:5000 in your browser.

Notes
- If you prefer `flask run`, set `FLASK_APP=app.py` and `FLASK_ENV=development`.
- Environment variables and secrets should go in a local `.env` file (already ignored by `.gitignore`).

Project layout (important files)

- `app.py` — Flask application entry
- `models.py` — SQLAlchemy models and DB setup
- `init_db.py` — helper to (re)create and seed the DB
- `requirements.txt` — Python dependencies
- `templates/` and `static/` — frontend assets and templates

Database
- By default the project uses SQLite (a `.db` file in project root). Change DB settings in `app.py` or `models.py` if needed.

Common tasks
- Re-seed DB: `python init_db.py`
- Update product prices script: `python update_prices.py`

Development tips
- Use a virtual environment per project to avoid global package conflicts.
- The repository `.gitignore` excludes local envs, IDE settings, and secrets.

Need anything else (deploy steps, Dockerfile, CI)? Open an issue or ask here.


