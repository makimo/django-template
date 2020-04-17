.PHONY: install-with-database database setup python js django initial-commit all

include Makefile

all: install-with-database initial-commit

install-with-database: database setup

database:
	createuser -P {{ cookiecutter.project_slug }}
	createdb -E utf8 {{ cookiecutter.project_slug }} -O {{ cookiecutter.project_slug }}

setup: python js django

python:
	python3 -m venv env
	env/bin/pip install -r requirements/local.txt

js:
	$(shell . ~/.nvm/nvm.sh; nvm exec 10 npm install 1>&2)
	$(shell . ~/.nvm/nvm.sh; nvm exec 10 npm run build 1>&2)

django: config
	env/bin/python manage.py migrate
	env/bin/python manage.py createsuperuser

initial-commit:
	git init
	git add --all
	git commit -am "Initial commit"

# vim: set noet:
