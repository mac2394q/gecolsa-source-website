#!/usr/bin/env bash
set -e

sudo -H pip install -r requirements.txt

python3.5 manage.py migrate --noinput

yarn install
gulp compile-sass

find . -name "*.pyc" -delete

python3.5 manage.py clear_cache
python3.5 manage.py collectstatic --noinput --ignore=*.sass

touch app/local_settings.py
sudo service celery restart
