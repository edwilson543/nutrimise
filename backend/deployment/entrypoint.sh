#!/usr/bin/env bash

python manage.py migrate
python manage.py collectstatic --noinput
DJANGO_SETTINGS_MODULE=nutrimise.config.settings DJANGO_CONFIGURATION=Settings gunicorn nutrimise.config.wsgi:application --bind 0.0.0.0:8000
