from django.apps import AppConfig


class TasklogicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasklogic'

    def ready(self):
        import tasklogic.signals
