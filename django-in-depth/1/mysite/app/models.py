from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    
    class Meta:
        permissions = [
            ('set_published_status', 'Can set the status of the post to either published or not'),
        ]