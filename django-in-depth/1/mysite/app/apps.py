from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    
    def ready(self):
        from app.signals import post_save, post_save_post, Post
        post_save.connect(post_save_post, sender=Post)
