#!/bin/sh

python manage.py makemigrations
python manage.py migrate
# python manage.py migrate --database=postgres
# python manage.py migrate --database=mysql
# python manage.py migrate --database=mongo

python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn middlevel.wsgi:application --bind 0.0.0.0:8000
