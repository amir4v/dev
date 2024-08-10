FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .
ENV PROJVARBLOG_SETTINGS_IN_DOCKER true

RUN set -xe \
    && apt update \
    && apt install -y --no-install-recommends build-essentials \
    && pip install poetry virtualenvwrapper \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry install --no-root

COPY ["README.md", "Makefile", "./"]
COPY core core
COPY local local

EXPOSE 8000

COPY scripts/entrypoint.sh ./entrypoint.sh
RUN chmod a+x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
