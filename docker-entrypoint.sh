#!/bin/sh
set -e
until cd /app
do
    echo "Waiting for server volume..."
done
until python manage.py migrate
do
    echo "Waiting for postgres ready..."
    sleep 2
done
python manage.py collectstatic --noinput

gunicorn globa.wsgi:application --bind 0.0.0.0:8787 --workers 4 --threads 4