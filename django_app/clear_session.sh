#!/bin/bash

rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# For PostgreSQL
#dropdb your_database_name
#createdb your_database_name

# For MySQL
#mysql -u your_username -p
#DROP DATABASE your_database_name;
#CREATE DATABASE your_database_name;

# Reset Redis
redis-cli FLUSHALL
#sudo systemctl restart redis    # ubuntu
brew services restart redis

# Recreate migrations and migrate
python manage.py makemigrations
python manage.py migrate

#python manage.py createsuperuser       # (optional) create superuser
#python manage.py collectstatic         # (optional) collect static files

# Finally
#python manage.py runserver