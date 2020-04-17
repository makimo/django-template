.PHONY: config deployconfig

ifeq (, $(shell which editor))
$(error "No editor in $(PATH), consider symlinking vim, emacs or nano.")
endif

config: {{ cookiecutter.project_slug }}/settings/db.py
deployconfig: {{ cookiecutter.project_slug }}/settings/email.py

{{ cookiecutter.project_slug }}/settings/db.py: {{ cookiecutter.project_slug }}/settings/db.py.base
	cp {{ cookiecutter.project_slug }}/settings/db.py.base {{ cookiecutter.project_slug }}/settings/db.py
	editor {{ cookiecutter.project_slug }}/settings/db.py

{{ cookiecutter.project_slug }}/settings/email.py: {{ cookiecutter.project_slug }}/settings/email.py.base
	cp {{ cookiecutter.project_slug }}/settings/email.py.base {{ cookiecutter.project_slug }}/settings/email.py
	editor {{ cookiecutter.project_slug }}/settings/email.py

# vim: set noet:
