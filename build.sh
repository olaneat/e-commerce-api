#!/usr/bin/env bash
apt-get update -qq && apt-get install -y libpq-dev python3-dev gcc g++ libssl-dev
pip install --no-cache-dir --force-reinstall --upgrade pip
pip install --no-cache-dir -r requirements.txt
python manage.py collectstatic --noinput