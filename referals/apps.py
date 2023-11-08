from django.apps import AppConfig


class ReferalsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "referals"

    def ready(self):
        import referals.signals
