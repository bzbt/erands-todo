from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone

from todos.models import Location, Task, Weather
from weather.api.client import WeatherApiClient


def refresh_weather(location: Location, task: Task | None) -> Weather:
    """
    Refreshes the weather for a location if it needs to be updated

    Args:
        location (Location): The location to get the weather for
        task     (Task):     The task object to get the weather from

    Returns:
        Weather: The weather object
    """
    if task is None or task.weather is None:
        data = WeatherApiClient().get_current_weather(location.latitude, location.longitude)
        return Weather().from_raw(data)

    ten_minutes_ago = timezone.now() - timedelta(minutes=10)

    if task.weather.updated < ten_minutes_ago:
        data = WeatherApiClient().get_current_weather(location.latitude, location.longitude)
        return Weather().from_raw(data, task.weather.id)

    if location.id != task.location.id:
        data = WeatherApiClient().get_current_weather(location.latitude, location.longitude)
        return Weather().from_raw(data, task.weather.id)

    return get_object_or_404(Weather, id=task.weather.id)
