import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ORM.ORM.settings')
django.setup()

from ORM.app.models import *
