from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.test import APISimpleTestCase
from rest_framework.test import APITransactionTestCase
from rest_framework.test import APIRequestFactory
from rest_framework import serializers
serializers.Serializer
serializers.ModelSerializer
serializers.ListSerializer
serializers.HyperlinkedModelSerializer
from rest_framework import fields
from rest_framework import routers
routers.DefaultRouter
routers.SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token, AuthTokenSerializer, ObtainAuthToken
from rest_framework.parsers import JSONParser, BaseParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework .response import Response, SimpleTemplateResponse
# `
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
User = get_user_model()
@receiver(post_save, sender=User, weak=False)
def report_uploaded(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
# in apps.py in app_nameConfig-Class:
def ready(self):
        # import app_name.signals
        pass
# `
