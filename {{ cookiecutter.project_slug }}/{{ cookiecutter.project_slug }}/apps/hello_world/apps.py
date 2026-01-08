from django.apps import AppConfig


class HelloWorldConfig(AppConfig):
    name = '{{ cookiecutter.project_slug }}.apps.hello_world'
