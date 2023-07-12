from django.urls import path

from .views import upload, upload_file, send_mail_to, login

urlpatterns= [
    path('login/', login, name='login'),
    path('', upload),
    path('upload_file', upload_file),
    path('send-mail/<str:subject>/<str:message>/<str:to>/', send_mail_to),
]