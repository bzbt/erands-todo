from django.apps import AppConfig


class WeatherConfig(AppConfig):
    """
    This class is used to configure the weather app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'
