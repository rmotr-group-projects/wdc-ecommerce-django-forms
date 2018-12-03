import os
import dj_database_url
from .base import *


SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    '^8ai-6gb!yyga81jugdahsi8a%c=)mb0xler7oW8lh1mz!^snago;91_')
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = ['*']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
