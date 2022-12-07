from django.urls import path
from .views import *
urlpatterns = [
    path('', Index.as_view()),
    path('t1', test1),
    path('t2', test2),
    path('t3', test3),
    path('t4', test4),
    path('tapi', testapi.as_view()),
    path('user-api', ListUsers.as_view()),
]
