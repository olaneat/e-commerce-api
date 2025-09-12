# commerce/settings/production.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'e-mrkt-api.onrender.com').split(',')

# Use Render's database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'e_market_ranu'),
#         'USER': os.environ.get('DB_USER', 'olaneat'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'TqEfX3jjfbzhvfaEkKiII83UQrNUIwjb'),
#         'HOST': os.environ.get('DB_HOST', 'dpg-d2j3p06mcj7s73ejpq8g-a.oregon-postgres.render.com'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

db_url = config('DB_URL')  # Use Render's provided variable
if not db_url:
    db_url = config('DB_URL')  # Fallback for local testing
if db_url:
    config = dj_database_url.parse(db_url)
    config['CONN_MAX_AGE'] = 600  # Set conn_max_age
    DATABASES['default'] = config
else:
    print("Warning: Neither DATABASE_URL nor DB_URL set, using default SQLite database.")
# Static and media files for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'