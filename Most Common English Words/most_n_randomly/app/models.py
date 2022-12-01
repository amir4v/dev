from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50)
    line = models.CharField(max_length=100)
    seen = models.IntegerField(default=0)