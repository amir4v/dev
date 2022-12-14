from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.query.QuerySet):
    def delete(self, sure=False):
        if sure:
            return super().delete()
        else:
            print('SOFT or HARD ?')
    
    def soft_delete(self):
        return self.update(soft_delete_dt=now())
    
    def hard_delete(self):
        return super().delete()
    
    def restore(self):
        return self.update(soft_delete_dt=None)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).all().filter(soft_delete_dt=None)
    
    def ALL(self):
        return super().get_queryset()
    
    def deleted(self):
        return super().get_queryset().exclude(soft_delete_dt=None)


class Model(models.Model):
    soft_delete_dt = models.DateTimeField(null=True, default=None, blank=True)
    objects = SoftDeleteManager()
    
    def delete(self, sure=False):
        if sure:
            return super().delete()
        else:
            print('SOFT or HARD ?')
    
    def soft_delete(self):
        self.soft_delete_dt = now()
        return self.save()
    
    def hard_delete(self):
        return super().delete()
    
    def restore(self):
        self.soft_delete_dt = None
        return self.save()


# ##################################################################################################
