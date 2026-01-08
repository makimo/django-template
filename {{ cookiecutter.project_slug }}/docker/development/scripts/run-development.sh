#!/bin/sh

set -e

MANAGE_PY=/app/manage.py
REQUIREMENTS=/app/requirements/local.txt

pip3 install -r $REQUIREMENTS
$MANAGE_PY migrate
$MANAGE_PY runserver 0.0.0.0:8000
