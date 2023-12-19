from django.apps import AppConfig
from django.apps import apps
from importlib import import_module


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp'

    def ready(self):
        import webapp.signals

