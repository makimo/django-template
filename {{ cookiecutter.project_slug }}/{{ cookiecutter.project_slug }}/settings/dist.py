from .base import *
from .email import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

ALLOWED_HOSTS = ['{{ cookiecutter.project_slug }}.makimo.pl', 'localhost']

# Admins
ADMINS = (
    ('Mateusz Papiernik', 'biuro@makimo.pl'),
)

MANAGERS = ADMINS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'json_formatter': {
            'class': '{{ cookiecutter.project_slug }}.apps.common.formatters.DjangoRequestJsonFormatter',
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console_json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter'
        }
    },
    'loggers': {
        'apps': {
            "level": "DEBUG",
            "handlers": ["console_json"],
        },
        'django': {
            'handlers': ["console_json"],
            'level': 'INFO',
            'propagate': True,
        }
    },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'dist')

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures', 'dist'),
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# Settings used to configurate whitenoise if needed
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ] + MIDDLEWARE
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Uncomment this if you want to allow logging to sentry from django app
# from .sentry import *
