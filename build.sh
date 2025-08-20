python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn commerce.wsgi:application --bind 0.0.0.0:8000