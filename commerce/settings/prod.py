# commerce/settings/production.py
from .base import *
import os
DEBUG = True
ALLOWED_HOSTS = [  'e-mrkt-api.onrender.com', 'localhost']
CORS_ALLOWED_ORIGINS = ['https://neatstorez.vercel.app', "http://localhost","http://localhost:5173"]
DATABASES = {
    'default': dj_database_url.config(
        default=config("PROD_DB_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}
DATABASES['default']['CONN_MAX_AGE'] = 600

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

# db_url = os.con('PROD_DB_URL')  # Use Render's provided variable
# if not db_url:
#     db_url = config('PROD_DB_URL')  # Fallback for local testing
# if db_url:
#     config = dj_database_url.parse(db_url)
#     config['CONN_MAX_AGE'] = 600  # Set conn_max_age
#     DATABASES['default'] = config
# Static and media files for Render
STATIC_ROOT = BASE_DIR / 'staticfiles_build'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'