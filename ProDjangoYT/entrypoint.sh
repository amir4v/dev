#!/usr/bin/env bash

# whichever brokes, break the whole system and don't try just power through them.
set -e

RUN_MANAGE_PY='poetry run python -m core.manage'

$RUN_MANAGE_PY collectstatic --no-input

$RUN_MANAGE_PY migrate --no-input

exec poetry run daphne project.core.asgi:application -p 8000 -b 0.0.0.0
