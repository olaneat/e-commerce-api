# commerce/settings/production.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'e-mrkt-api.onrender.com']
# Use Render's database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'e_market_ranu'),
#         'USER': os.environ.get('DB_USER', 'olaneat'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'TqEfX3jjfbzhvfaEkKiII83UQrNUIwjb'),
#         'HOST': os.environ.get('DB_HOST', 'dpg-d2j3p06mcj7s73ejpq8g-a.oregon-postgres.render.com'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }.
# }

db_url = config('DB_URL')  # Use Render's provided variable
print("Database URL:", db_url)  # Debugging line
if not db_url:
    db_url = config('DB_URL')  # Fallback for local testing
if db_url:
    config = dj_database_url.parse(db_url)
    print("Database configuration:", config)  # Debugging line
    config['CONN_MAX_AGE'] = 600  # Set conn_max_age
    DATABASES['default'] = config
# Static and media files for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'