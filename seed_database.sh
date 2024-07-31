#!/bin/bash

rm db.sqlite3
rm -rf ./fixapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations fixapi
python3 manage.py migrate fixapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata customers
python3 manage.py loaddata categories
python3 manage.py loaddata contractors
python3 manage.py loaddata servicerequests
python3 manage.py loaddata servicerequestcategories
python3 manage.py loaddata notifications

