#!/usr/bin/env bash
echo "DEBUG: Starting build process at $(date)"
apt-get update -qq && apt-get install -y libpq-dev python3-dev gcc g++ libssl-dev
echo "DEBUG: Installed system dependencies at $(date)"
pip install --no-cache-dir --force-reinstall --upgrade pip
pip install --no-cache-dir -r requirements.txt
echo "DEBUG: Installed Python dependencies at $(date)"
echo "DEBUG: Environment - SUPERUSER_EMAIL=$SUPERUSER_EMAIL, SUPERUSER_USERNAME=$SUPERUSER_USERNAME, SUPERUSER_PASSWORD=***, SUPERUSER_ROLE=$SUPERUSER_ROLE"
python manage.py migrate --noinput || echo "DEBUG: Migration failed at $(date) with exit code $?"
echo "DEBUG: Migration attempted at $(date)"
python manage.py collectstatic --noinput --ignore '*.pyc' --ignore '*.log' || echo "DEBUG: Collectstatic failed at $(date) with exit code $?"
echo "DEBUG: Build completed at $(date)"