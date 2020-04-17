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
    },
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, 'logs', 'debug.log'),
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, 'logs', 'info.log'),
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    'loggers': {
        'apps': {
            "level": "DEBUG",
            "handlers": ["debug_file_handler", "info_file_handler"],
        },
        'django': {
            'handlers': ["debug_file_handler", "info_file_handler"],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
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

WEBPACK_MANIFEST_FILE = os.path.join(BASE_DIR, '../webpack-stats.dist.json')
