from django.urls import path
from .views import home, refresh


urlpatterns = [
    path('', home),
    path('refresh/', refresh),
]