import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ORM.settings')
django.setup()

from app.models import *
