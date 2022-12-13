from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'


# from django.core.signals import request_started, request_finished
# from django.dispatch import receiver
# from django.db.models.signals import *


# def my_call_back(sender, *a, **k):
#     print('my_call_back')
#     print(*a)
#     print(k)
#     # print(sender, *a, **k)


# request_started.connect(my_call_back)
# request_finished.connect(my_call_back)
