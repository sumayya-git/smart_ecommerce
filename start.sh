#!/bin/sh

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
gunicorn ecommerce_project.wsgi:application \
    --bind 127.0.0.1:8000 &

echo "Starting Nginx..."
nginx -g "daemon off;"