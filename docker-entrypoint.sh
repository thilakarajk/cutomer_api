#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Creating static files"
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
gunicorn -b :8000 --workers=3 customer_api.wsgi:application