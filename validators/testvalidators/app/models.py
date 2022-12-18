from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()
