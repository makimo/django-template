# Manual Installation

This guide covers setting up the project without Docker.

## Prerequisites

### Database

```
createuser -P {{ cookiecutter.project_slug }}
createdb -E utf8 {{ cookiecutter.project_slug }} -O {{ cookiecutter.project_slug }}
```

### Node

To install nvm use official guide https://github.com/creationix/nvm#install--update-script.

If you are using zsh shell you can use one of those guides to make nvm work inside shell:

* https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins/nvm
* https://github.com/lukechilds/zsh-nvm

After setup nvm you can use this command to install specific node package
```
nvm install 22
```

To choose one of installed nvm version type:
```
$ nvm use 22
Now using node v22.x.x (npm vX.X.X)
```

## Setup

### Python
```
python3 -m venv env
source env/bin/activate
pip install -r requirements/local.txt // or requirements/dist.txt in production environment
```

### Environment variables

You should copy `.env.example` file with following command:
```
cp .env.example .env
```
and populate it with your options.

### JS Stack
```
npm install
npm run watch // or npm run build for one-time compilation
```

If you want to build production assets, use:
```
npm run build-dist
```

### Django

Copy the `{{ cookiecutter.project_slug }}/settings/db.py.base` to
`{{ cookiecutter.project_slug }}/settings/db.py` and modify it to your needs,
then run:

```
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

## Notes for deploy

Copy the `{{ cookiecutter.project_slug }}/settings/email.py.base` to
`{{ cookiecutter.project_slug }}/settings/email.py` and modify it to your needs.

1. Ensure that `DJANGODIR` in `bin/gunicorn.base` is proper.

### Whitenoise

To use whitenoise in production you should uncomment whitenoise package in `requirements/dist.txt`
and uncomment following code:
```python
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
# ] + MIDDLEWARE
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
in `dist.py` settings

### Sentry

First you should create new Sentry project (https://sentry.io/)[https://sentry.io/].
If you've done it already you have to find `DSN` URL for the project.
To do that you have to open project setting and in `SDK Setup` tab,
click at `Client Keys (DSN)` and copy the DSN to environment variable called `SENTRY_DSN`.

#### Django

If you want to enable Sentry logging for Django app you should uncomment
`sentry-sdk` in the `dist` requirements and uncomment module import:
`from .sentry import *` in `dist.py`. Also you can use `SENTRY_SEND_PII` variable
to change if user object should be attached to the Sentry log or not.

#### Vue

If you want to enable Sentry logging for Vue app you should add following import to your
starting point:
```js
import './../scripts/sentry.js';
```
and change `<DSN>` property in the `sentry.js` file.

If you want to verify the installation, just generate random error and
you should see new issue in the sentry project's page.
For more information about Sentry go to the docs page:
[https://docs.sentry.io/](https://docs.sentry.io/)
