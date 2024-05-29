import pytest

from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from todos.models import Location, Weather, Task
from todos.utils import refresh_weather
from weather.api.client import RawWeather, WeatherApiClient


# Define a sample response to return when the method is called
def mock_raw_weather(lat, lon):
    return Weather().from_raw(
        RawWeather(
            temperature=320.0,
            humidity=50,
            condition=800,
            latitude=lat,
            longitude=lon,
        )
    )


class TestRefreshWeather(TestCase):

    def setUp(self):
        call_command('loaddata', 'todos/tests/fixtures/db.yaml')

    def tearDown(self):
        call_command('flush', interactive=False)


    @patch.object(WeatherApiClient, 'get_current_weather', side_effect=mock_raw_weather)
    def test_refresh_weather__fetch_new_no_task(self, mock_get_current_weather):
        location = Location.objects.get(id=2)
        mock_get_current_weather.return_value = mock_raw_weather(location.latitude, location.longitude)

        weather = refresh_weather(location, None)
        mock_get_current_weather.assert_called_once_with(location.latitude, location.longitude)
        self.assertEqual(str(weather), str(mock_raw_weather(location.latitude, location.longitude)))

    @patch.object(WeatherApiClient, 'get_current_weather', side_effect=mock_raw_weather)
    def test_refresh_weather__fetch_new_as_is_oudated(self, mock_get_current_weather):
        location = Location.objects.get(id=3)
        mock_get_current_weather.return_value = mock_raw_weather(location.latitude, location.longitude)

        weather = refresh_weather(location, Task.objects.get(id=2))
        mock_get_current_weather.assert_called_once_with(location.latitude, location.longitude)
        self.assertEqual(str(weather), str(mock_raw_weather(location.latitude, location.longitude)))

    @patch.object(WeatherApiClient, 'get_current_weather', side_effect=mock_raw_weather)
    def test_refresh_weather__fetch_new_for_new_location(self, mock_get_current_weather):
        location = Location.objects.get(id=3)
        task = Task.objects.get(id=2)
        task.weather.updated = timezone.now() - timezone.timedelta(minutes=2)
        mock_get_current_weather.return_value = mock_raw_weather(location.latitude, location.longitude)

        weather = refresh_weather(location, task)
        mock_get_current_weather.assert_called_once_with(location.latitude, location.longitude)
        self.assertEqual(str(weather), str(mock_raw_weather(location.latitude, location.longitude)))

    @patch.object(WeatherApiClient, 'get_current_weather', side_effect=mock_raw_weather)
    def test_refresh_weather__return_existing(self, mock_get_current_weather):
        location = Location.objects.get(id=3)
        task = Task.objects.get(id=1)
        task.weather.updated = timezone.now() - timezone.timedelta(minutes=2)

        weather = refresh_weather(location, task)
        mock_get_current_weather.assert_not_called()
        self.assertEqual(str(weather), str(task.weather))
