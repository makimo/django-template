import os

project_slug_upper = "{{ cookiecutter.project_slug_upper }}"
db_name = os.environ[f'{project_slug_upper}_DB_NAME']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_name,
        'USER': os.environ[f'{project_slug_upper}_DB_USER'],
        'PASSWORD': os.environ[f'{project_slug_upper}_DB_PASSWORD'],
        'HOST': os.environ[f'{project_slug_upper}_DB_HOST'],
        'PORT': os.environ[f'{project_slug_upper}_DB_PORT'],
        'TEST': {
            'CHARSET': 'UTF8',
            'NAME': f'{db_name}-test'
        }
    }
}
