from django.apps import AppConfig


class MainwebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainwebsite'
    
    def ready(self):
        from . import signals
        from .templatetags import auth_extras, custom_filters, param_replace

        from .models import MODELS_TO_AUDIT
        
        for model in MODELS_TO_AUDIT:
            signals.track_model(model)