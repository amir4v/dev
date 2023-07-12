from django.urls import path

from .views import upload, upload_file, send_mail_to, login, search, add_car, SearchCars

urlpatterns= [
    path('login/', login, name='login'),
    path('', upload),
    path('upload_file', upload_file),
    path('send-mail/<str:subject>/<str:message>/<str:to>/', send_mail_to),
    path('add-car/<str:name>/', add_car, name='add-car'),
    path('search-cars/<str:query>/', SearchCars.as_view(), name='search-cars'),
    path('search/', search, name='search'),
]