"""
README
------
For changing the models:
    - cd ORM
    - in settings.py/INSTALLED_APPS and app/apps.py :
        - Uncomment/Comment the name you need.
    - python manage.py makemigrations
    - python manage.py makemigrations app
    - python manage.py migrate
    - in settings.py/INSTALLED_APPS and app/apps.py :
        - Uncomment/Comment the name you need.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ORM.ORM.settings')
django.setup()

from ORM.app.models import *
