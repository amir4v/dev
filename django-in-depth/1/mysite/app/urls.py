from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect

from . import views


def _logout(request):
    logout(request)
    return redirect('/')


urlpatterns = [
    path('', views.HomeView.as_view()),
    # path('', views.home),
    path('logout', _logout),
]
