"""
CI/CD settings for automated testing.

Uses environment variables for database configuration.
"""
from .base import *

DATABASES = {
    'default': env.db(),
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = False

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'local')
]

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures', 'tests'),
    os.path.join(BASE_DIR, 'fixtures', 'dist'),
]
