import os

import dj_database_url

DATABASES = {}
DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL', 'postgres://'), conn_max_age=600)
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
