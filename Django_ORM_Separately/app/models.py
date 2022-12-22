from django.db import models


class ModelName(models.Model):
    field = models.TextField()
    
    def clean(self) -> None:
        print('clean')
        return super().clean()
    
    def clean_fields(self, exclude):
        print('clean_fields')
        return super().clean_fields(exclude)
    
    def clean_field(self):
        print('field')
