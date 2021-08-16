from django.apps import AppConfig


class AppStorageConfig(AppConfig):
    name = 'app_storage'
    verbose_name = 'Работа со складом'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import app_storage.signals.handlers