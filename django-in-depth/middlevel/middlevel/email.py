
# from time import sleep

# from django.core.mail import send_mail

# from celery import shared_task

# @shared_task
# def _do_send_mail(subject='subjct', message='msg', from_email='me@er.cdf', recipient_list=['yo@ho.co'],
#                 fail_silently=False, auth_user=None, auth_password=None,
#                 connection=None, html_message=None):
#     sleep(3)
#     subject = 'test'
#     message = 'testing message...'
#     from_email = 'admin@admin.admin'
#     recipient_list = ['to@user.site.com']
#     send_mail(subject, message, from_email, recipient_list,
#               fail_silently, auth_user, auth_password,
#               connection, html_message)