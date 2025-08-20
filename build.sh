#!/usr/bin/env bash
apt-get update -qq && apt-get install -y libpq-dev python3-dev libjpeg-dev zlib1g-dev
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput