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

Test dependencies are included in `requirements.txt`. To run the test suite locally, first activate your virtual environment and install dependencies, then run tests using `pytest` or Django's test runner.

Example (local):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
# run all tests with pytest
pytest
# or run Django's test runner
python manage.py test
```

Run a single test file or test case with pytest:

```bash
pytest products/tests.py::TestProductModel::test_product_str
```

Collect coverage (optional, if `coverage` is installed):

```bash
coverage run -m pytest
coverage report -m
```

Running tests inside Docker (compose):

```bash
docker compose run --rm web python manage.py test
```

## CI / CD (high level)

This project is designed to be included in a CI/CD pipeline (GitHub Actions). A typical pipeline includes the following jobs:

- lint: run linters such as `flake8` and optionally formatting checks (`black --check`).
- test: install dependencies, run migrations (or use an in-memory/test DB), and execute the test suite with `pytest` or `manage.py test`.
- build: build the Docker image using the provided `Dockerfile`.
- publish: push the built image to a container registry (Docker Hub, GitHub Container Registry, etc.).
- deploy: deploy the image to your hosting platform (Kubernetes, ECS, a PaaS, or a VM).

A minimal GitHub Actions workflow would:

1. Checkout the code
2. Set up Python
3. Install dependencies
4. Run lint and tests
5. Build and (optionally) push Docker image on branch protection or tag events

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
