FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput && gunicorn ipswich_retail.wsgi:application --bind 0.0.0.0:8000"]
