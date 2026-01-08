# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## Quick Start

### Prerequisites

* `docker` (20.10.0+)
* `docker compose` (2.0.0+)

### Running the project

Enter:

```
docker compose -f docker/development/docker-compose.yml up
```

The application will be available at `http://localhost:8000`. The
database will be spawned, the migrations will be run automatically, all
deps installed (for both Python and JS) and the code will be
automatically reloaded when changes occur (for both assets and backend code).

### Running commands in the container

To run commands in the running container (for instance: installing new
packages, running tests, running Django commands etc.) please run in a
separate terminal window (while `docker compose up` is running):

```
docker compose -f docker/development/docker-compose.yml exec {{ cookiecutter.project_slug }}-backend python manage.py [command]
```

> For manual installation without Docker, see [docs/manual_install.md](docs/manual_install.md).

## Development

### Code Quality

This project uses pre-commit hooks for code formatting:

```
pip install pre-commit
pre-commit install
```

Tools used:
- **black** - Python code formatter
- **isort** - Python import sorter

### Testing

Run tests with the following command:

```
docker compose -f docker/development/docker-compose.yml python manage.py test
```

## CI/CD

This project includes GitHub Actions workflows:

- **quality.yml** - Code quality checks with PySCN
- **test.yml** - Automated testing with PostgreSQL
- **deploy.yml** - Production deployment (manual trigger)

## Bundled Modules

- [GDPR](docs/GDPR.md) - Vue modal privacy settings window with utilities to comply with GDPR.

## More Information

This project was created using [django-template](https://github.com/makimo/django-template).
