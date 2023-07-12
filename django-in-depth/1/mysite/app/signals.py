from django.contrib.auth.models import User
from django.db.models.signals import class_prepared, m2m_changed, post_delete, \
                                     post_init, pre_delete, post_save, post_migrate, \
                                     pre_init, pre_migrate, pre_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def post_save_post(sender, instance, created, *args, **kwargs):
    print(sender)
    print(instance.title, '-', instance.content)
