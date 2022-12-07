from django.db import models


class Memory(models.Model):
    ip = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
    throttle = models.CharField(max_length=200, null=True, default=None) # n_t_t


class View(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
    limit = models.CharField(max_length=50, null=True, default=None) # n/n:duration
#
#
class ViewMemory(models.Model):
    ip = models.CharField(max_length=100, unique=True, db_index=True, null=False, blank=False)
    throttle = models.CharField(max_length=200, null=True, default=None) # n_t_t
    
    view = models.ForeignKey(View, null=True, default=None, on_delete=models.CASCADE, related_name='view_memories')
