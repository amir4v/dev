import os
import sys
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_ORM_Separately.settings')
django.setup()


from app import models
