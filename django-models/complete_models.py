from django.db import models
from django.utils.timezone import now
from django.core.mail import send_mail
from softdelete_models import SoftDeleteModel
from helper import random_str


class CompleteModel(SoftDeleteModel):
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)
    
    is_active = models.BooleanField(default=True)
    
    signature = models.CharField(max_length=100, default=random_str, unique=True, db_index=True)


class UserModel(CompleteModel):
    # from django.contrib.auth.models import User
    
    # Any Characters
    name = models.CharField(max_length=100, blank=True)
    
    # ASCII Characters, LowerCase==UpperCase
    # Digits
    # Under_Score, Not Allow To Use Tow _ Continuous
    # At Least Must Contain One ASCII Character
    # Minimum Length is 6
    # Maximum Length is 16
    username = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Any Characters
    password = models.CharField(max_length=100)
    
    # Email
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    
    def __str__(self):
        return f'@{self.username}'
    
    def clean(self):
        super().clean()
        #TODO
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
