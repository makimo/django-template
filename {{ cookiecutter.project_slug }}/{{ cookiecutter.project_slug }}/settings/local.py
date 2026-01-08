DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ cookiecutter.project_slug }}',
        'USER': '{{ cookiecutter.project_slug }}',
        'PASSWORD': 'secret',
        'HOST': '{{ cookiecutter.project_slug }}-db',
        'PORT': '5432',
        'TEST': {
            'CHARSET': 'UTF8',
            'NAME': '{{ cookiecutter.project_slug }}-test'
        }
    }
}

from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True

INSTALLED_APPS += ('debug_toolbar',)

DEBUG_TOOLBAR_PATCH_SETTINGS = False

VALIDATE_FRONT_PASSWORD = False

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'local')
]

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures', 'tests'),
    os.path.join(BASE_DIR, 'fixtures', 'dev'),
    os.path.join(BASE_DIR, 'fixtures', 'dist'),
]

INTERNAL_IPS = [
    '0.0.0.0',
    '127.0.0.1'
]

