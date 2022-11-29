from django.db import models


class Link(models.Model):
    url = models.CharField(max_length=5000, unique=True, db_index=True, blank=False, null=False)
    seen = models.BooleanField(default=False)