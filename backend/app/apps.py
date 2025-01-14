from django.apps import AppConfig # Import the AppConfig class for configuring the Django app

class ModerationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Set the default auto field for models in this app

    name = 'app'  
