FROM python:3.10.5-buster

WORKDIR /opt/project

# prevents python to create .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# is going to disable python's input output buffering
ENV PYTHONUNBUFFERED 1
# adds current working directory to python's path
ENV PYTHONPATH .
ENV CORESETTINGS_IN_DOCKER true

RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essentials \
    && pip install virtualenvwrapper poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry install --no-root

COPY ["README.md", "Makefile", "./"]
COPY core core
COPY local local

EXPOSE 8000

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
