# commerce/settings/local.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost']
CORS_ALLOWED_ORIGINS = [ "http://localhost:5173"]

# Use a local database (e.g., SQLite for development)
DATABASES = {
    # "default": dj_database_url.parse(os.environ.get('DB_URL'))
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER':config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT')
    }
}
