from time import sleep, time
import os

# from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from celery import shared_task
from mail_templated import send_mail
# from mail_templated import EmailMessage


@shared_task
def do_send_mail(subject, message, to):
    open(settings.BASE_DIR / 'BackgroundProcess.log', 'a').write(str(time()) + '\n')
    sleep(1)
    open(settings.BASE_DIR / 'BackgroundProcess.log', 'a').write(str(time()) + '\n')
    sleep(1)
    
    send_mail('email.tpl', {'name': 'Smaan Golriz'}, settings.EMAIL_HOST_USER,recipient_list=[to])
    #   ####   ######  #####  ######    #######    #######   ######3
    # message = EmailMessage(template_name='email.tpl', context={'name': 'AmirHosein Ghorbani'}, from_email=settings.EMAIL_HOST_USER, to=[to])
    # message.send()
    #   ####   ######  #####  ######    #######    #######   ######3
    # message = EmailMessage(template_name='email.tpl', context={'name': 'Sohrab Sepehri'}, from_email=settings.EMAIL_HOST_USER, to=[to])
    # message.attach_file(
    #     os.path.join(settings.BASE_DIR,'media/images/pictures/Screenshot_20230203-132216_Instagram.jpg'),
    #     'image/jpeg')
    # message.send()
    #   ####   ######  #####  ######    #######    #######   ######3
    
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to])
    mail.attach('File-Name.jpg', 
                open(os.path.join(settings.BASE_DIR,'media/images/pictures/Screenshot_20230203-132216_Instagram.jpg'), 'rb').read(),
                'image/jpeg')
    mail.send()
    
    # send_mail(subject, message, settings.EMAIL_HOST_USER, [to], html_message="""
    #           <h1>HELLO</h1>
    #           <p>hi</p>
    #           <small>small</small>
    #           <i>i-small</i>
    #           <br>
    #           <strong>YOOOO.!</strong>
    #           """)