# commerce/settings/production.py
from .base import *
import os
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'neat-storez-api-env.eba-zavhb3km.us-west-2.elasticbeanstalk.com', 'https://neatstorez.vercel.app/']
CORS_ALLOWED_ORIGINS = ['https://neatstorez.vercel.app']

# Use AWS's database
# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
#         'NAME': os.environ.get('AWS_DB_NAME') or os.environ.get('DB_NAME'),
#         'USER': os.environ.get('AWS_DB_USER') or os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('AWS_DB_PASSWORD') or os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('AWS_DB_HOST') or os.environ.get('DB_HOST'),
#         'PORT': os.environ.get('AWS_DB_PORT') or os.environ.get('DB_PORT', '5432'),
#         'OPTIONS': {'sslmode': 'require'} if 'rds.amazonaws.com' in (os.environ.get('AWS_DB_HOST') or '') else {}
#     }
# }

db_url = config('PROD_DB_URL')  # Use Render's provided variable
if not db_url:
    db_url = config('PROD_DB_URL')  # Fallback for local testing
if db_url:
    config = dj_database_url.parse(db_url)
    config['CONN_MAX_AGE'] = 600  # Set conn_max_age
    DATABASES['default'] = config
# Static and media files for Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'