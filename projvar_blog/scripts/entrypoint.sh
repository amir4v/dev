#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m core.manage'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migratye --no-input

echo 'Running local server...'
$RUN_MANAGE_PY runserver 0.0.0.0:8000

# Production server (gunicorn + nginx + daphne)

# exec poetry run daphne core.core.asgi:application -p 8000 -b 0.0.0.0
