#!/bin/bash

rm db.sqlite3
rm -rf ./fixapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations fixapi
python3 manage.py migrate fixapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

