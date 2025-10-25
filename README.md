# Ipswich Retail — Django Proof of Concept

A small Django-based proof of concept e-commerce app (products, orders, cart) with both a lightweight local development setup (SQLite) and a Docker/Docker Compose production-like setup (Postgres + Gunicorn).

## What's included

- A Django project in `ipswich_retail/` and two apps: `products/` and `orders/`.
- A sample management command to seed demo product data: `products.management.commands.seed_data`.
- `Dockerfile` and `docker-compose.yml` for containerized runs using Postgres and Gunicorn.

## Requirements

- macOS / Linux / Windows WSL
- Python 3.11 (project Dockerfile uses 3.11; local Python 3.10+ should work with Django 4.2+)
- pip
- (Optional) Docker & Docker Compose for containerized runs

The project uses Django >=4.2 (see `requirements.txt`).

## Quick start — Local (recommended for development)

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install runtime requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. (Optional) Create a superuser to access the admin:

```bash
python manage.py createsuperuser
```

5. Seed sample product data (provides categories and sample products):

```bash
python manage.py seed_data
```

6. Run the development server:

```bash
python manage.py runserver
# Visit http://127.0.0.1:8000
```

Notes:
- By default the project uses SQLite (`db.sqlite3`) for local runs (see `ipswich_retail/settings.py`).
- Environment variables are read via `django-environ`. If you need to change secrets or DB settings locally, create a `.env` file in the project root and set values like `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`.

## Quick start — Docker (Postgres + Gunicorn)

The repository includes a `Dockerfile` and `docker-compose.yml` to run the app with Postgres and Gunicorn.

1. (Optional) Create a `.env` file in the repo root with at least the following entries (or rely on the compose defaults):

```env
SECRET_KEY=change-me
DEBUG=True
POSTGRES_DB=ipswich_db
POSTGRES_USER=ipswich_user
POSTGRES_PASSWORD=ipswich_pass
ALLOWED_HOSTS=127.0.0.1,localhost
```

2. Start with Docker Compose:

```bash
docker compose up --build
```

3. The web app will be available at http://127.0.0.1:8000 (Gunicorn binds to 0.0.0.0:8000 per the `Dockerfile`).

Notes about Docker setup:
- `docker-compose.yml` defines a `db` (Postgres) service and a `web` service. The web service depends on the DB.
- If you want to run migrations inside the running container, open a shell into the `web` container and run `python manage.py migrate` (or add a startup step to your compose workflow).

## Running tests

Install test requirements and run pytest:

```bash
pip install -r requirements-test.txt
pytest
```

## Common management commands

- Apply migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Collect static files (for production): `python manage.py collectstatic --noinput`
- Seed sample data: `python manage.py seed_data`

## Project structure (high level)

- `ipswich_retail/` — Django project settings, URL conf, WSGI/ASGI
- `products/` — products app (models, views, templates)
- `orders/` — orders app
- `templates/`, `static/` — UI templates and assets
- `Dockerfile`, `docker-compose.yml` — containerized runtime

## Notes & troubleshooting

- If you change DB engine or credentials, update `.env` and re-run migrations.
- If the database is empty and you want sample data, run `python manage.py seed_data`.
- In Docker mode, the compose file uses Postgres; local development defaults to SQLite to keep setup lightweight.

Enjoy exploring the project!
