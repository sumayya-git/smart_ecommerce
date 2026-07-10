#!/bin/sh
set -e

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Setting nginx port..."
sed -i "s/listen 80;/listen ${PORT};/" /etc/nginx/conf.d/default.conf

echo "Starting Gunicorn..."
gunicorn ecommerce_project.wsgi:application \
    --bind 0.0.0:0:${PORT} \
    --workers 1 \
    --timeout 120 \
    --log-level debug 

# echo "Starting Nginx..."
# exec nginx -g "daemon off;"