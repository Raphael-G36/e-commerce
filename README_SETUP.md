# E-Commerce Site (Flask + SQLAlchemy)

Lightweight e-commerce demo built with Flask and SQLAlchemy.

## Quick setup & run

1) Create a virtual environment (recommended)

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
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

If you'd like, I can replace the existing `README.md` with this clean version now.
