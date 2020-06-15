# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Installation

> Note: if you are a lazy hog, please scroll down to the "Docker" section.

### Prerequisites

#### Database

```
createuser -P {{ cookiecutter.project_slug }}
createdb -E utf8 {{ cookiecutter.project_slug }} -O {{ cookiecutter.project_slug }}
```

#### Node
To install nvm use official guide https://github.com/creationix/nvm#install--update-script.

If you are using zsh shell you can use one of those guides to make nvm work inside shell:

* https://github.com/robbyrussell/oh-my-zsh/tree/master/plugins/nvm
* https://github.com/lukechilds/zsh-nvm

After setup nvm you can use this command to install specific node package
```
nvm install 10
```

To choose one of installed nvm version type:
```
$ nvm use 10
Now using node v10.10.0 (npm v6.4.1)
```

### Setup

#### Python
```
python3 -m venv env
source env/bin/activate
pip install -r requirements/local.txt // or requirements/dist.txt in production environment
```

#### Environment variables
You should copy `.env.example` file with following command:
```
cp .env .env.example
```
and populate it with your options.

#### JS Stack
```
npm install
npm run watch-assets // or npm run build for one-time compilation
```

If you want to build production assets, use:
```
npm run build-dist
```

#### Django

Provided that `editor` symlinks to vim, emacs or nano:

```
make config
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Alternatively, copy the `{{ cookiecutter.project_slug }}/settings/db.py.base` to
`{{ cookiecutter.project_slug }}/settings/db.py` and modify it to your needs,
then run the rest of the commands.

### Notes for deploy

Provided that `editor` symlinks to actual editor:
```
make deployconfig
```

Alternatively, copy the `{{ cookiecutter.project_slug }}/settings/email.py.base` to
`{{ cookiecutter.project_slug }}/settings/email.py` and modify it to your needs,
then run the rest of the commands.

1. Ensure that `DJANGODIR` in `bin/gunicorn.base` is proper.
2. Ensure that paths in `webpack-stats.dist.json` are proper (path is
configured in `package.json`).


#### More information
This project was created using `django-template` tool.

For more information, see:
https://bitbucket.org/makimo/django-template/src/master/.
If you find a bug, create an issue as a subtask of IWM-47.

#### Bundled Modules

GDPR [GDPR](docs/GDPR.md) - a Vue modal privacy settings window with 
a set of utilities  to comply with the European Union General Data 
Protection Regulation.

## Docker

### Prerequisites

To run this project in dockerized development environment the following
dependencies must be present in the system:

* `docker` (18.06.0+)
* `docker-compose` (1.22.0+)

### Running the project in development mode

This project supports dockerized development environment, so you
actually don't need to do any of the above steps. To run the project in
dockerized mode enter the `docker/development` directory and run:

```
docker-compose up
```

The application will be available at `http://localhost:8000`. The
database will be spawned, the migrations will be run automatically, all
deps installed (for both Python and JS) and the code will be
automatically reloaded when changes occur (for both assets and backend code).

### Running commands in the container

To run commands in the running container (for instance: installing new
packages, running tests, running Django commands etc.) please run in the
separate terminal window (while `docker-compose up` is running) the
following command:

```
docker-compose exec {{ cookiecutter.project_slug }}-backend bash
```

This will start interactive `bash` session that will allow running all
the commands within running container.

