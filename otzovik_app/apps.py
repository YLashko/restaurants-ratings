from django.apps import AppConfig


class OtzovikConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otzovik_app'

    def ready(self):
        print("Server started")
