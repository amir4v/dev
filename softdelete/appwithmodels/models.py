from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.query.QuerySet):
    pass


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(soft_delete=None)
    
    def ALL(self):
        return super().get_queryset()


class TableName(models.Model):
    field = models.TextField()
    
    def __str__(self):
        return self.field
    
    #
    
    soft_delete = models.DateTimeField(null=True, default=None, blank=True)
    objects = SoftDeleteManager()
    
    def delete(self, *a, **k):
        self.soft_delete = now()
        return self.save()
    
    def restore(self, *a, **k):
        self.soft_delete = None
        return self.save()
    
    def hard_delete(self, *a, **k):
        return self.__class__.objects.get(pk=self.pk).delete()
