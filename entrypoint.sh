#!/bin/bash

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic

# migrate
echo "yes"
echo "migrate"
python3 manage.py makemigrations
python3 manage.py migrate


# Start server
echo "Starting server"

#python3 manage.py runserver 0.0.0.0:8000
#gunicorn --env DJANGO_SETTINGS_MODULE=config.settings config.wsgi:application --bind 0.0.0.0:8000
#gunicorn config.wsgi
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload


exec "$@"
