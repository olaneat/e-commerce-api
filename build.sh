#!/usr/bin/env bash
apt-get update -qq && apt-get install -y libpq-dev python3-dev gcc g++ libssl-dev
pip install --no-cache-dir --force-reinstall --upgrade pip
pip install --no-cache-dir -r requirements.txt
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='${SUPERUSER_USERNAME}').delete(); User.objects.create_superuser('${SUPERUSER_USERNAME}', '${SUPERUSER_EMAIL}', '${SUPERUSER_PASSWORD}')" | python manage.py shell
python manage.py collectstatic --noinput --ignore '*.pyc' --ignore '*.log'