import os
from __future__ import absolute_import, unicode_literals

from celery import Celery

# Set deafule Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery()

# Use settings from the settings file with a CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()
