from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # name = 'app' # For changing the models
    name = 'ORM.app' # For using the models in the proxy
