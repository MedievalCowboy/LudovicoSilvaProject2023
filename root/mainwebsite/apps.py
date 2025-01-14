from django.apps import AppConfig


class MainwebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainwebsite'
    
    def ready(self):
        from . import signals
