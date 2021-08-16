from django.apps import AppConfig


class AppDocumentsConfig(AppConfig):
    name = 'app_documents'
    verbose_name = 'Работа с продажами'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import app_documents.signals.handlers
