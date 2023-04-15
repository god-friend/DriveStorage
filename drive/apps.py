from django.apps import AppConfig
from django.core.signals import setting_changed

class DriveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drive'

    def ready(self) -> None:
        import drive.signals
