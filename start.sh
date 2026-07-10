#!/bin/sh
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Setting nginx port..."
sed -i "s/listen 80;/listen ${PORT};/" /etc/nginx/conf.d/default.conf

echo "Starting Celery Worker..."
celery -A ecommerce_project worker --loglevel=info &

echo "Starting Gunicorn..."
gunicorn ecommerce_project.wsgi:application \
    --bind 127.0.0.1:8000 &

sleep 3

echo "Starting Nginx..."
nginx -g "daemon off;"