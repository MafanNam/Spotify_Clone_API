#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

# run a worker celery beat :)
celery -A config.celery beat -l info
