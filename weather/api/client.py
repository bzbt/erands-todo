from collections import namedtuple
import requests
from django.conf import settings

from weather.apps import WeatherConfig

RawWeather = namedtuple(
    'RawWeather',
    [
        'temperature', # in Kelvin
        'humidity',    # in percent
        'condition',   # weather condition code
        'latitude',    # latitude of the location
        'longitude',   # longitude of the location
    ]
)


class WeatherApiClient:
    """
    A client for the OpenWeather API

    Attributes:
        api_key           (str): The OpenWeather API key, obtained from project settings
        base_url          (str): The base URL for the OpenWeather API
        geocoding_api_url (str): The URL for the OpenWeather Geocoding API
    """

    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.geocoding_api_url = "https://api.openweathermap.org/geo/1.0/direct"

    def get_current_weather(self, latitude: float, longitude: float) -> RawWeather:
        """
        Get the weather data for a location

        Args:
            latitude  (float): The latitude of the location
            longitude (float): The longitude of the location

        Returns:
            RawWeather: The raw weather data
        """
        params = {
            "appid": self.api_key,
            "exclude": "minutely,hourly,daily,alerts",
            "lat": latitude,
            "lon": longitude,
        }
        data = self.make_get_request(params)

        weather = RawWeather(
            temperature=data["current"]["temp"],
            humidity=data["current"]["humidity"],
            condition=data["current"]["weather"][0]["id"],
            latitude=latitude,
            longitude=longitude,
        )

        return weather

    def make_get_request(self, params) -> dict:
        """
        Make a GET request to the OpenWeather API

        Args:
            params (dict[str, str]: The query parameters

        Returns:
            dict: The JSON response
        """
        response = requests.get(self.base_url, params=params)

        if response.status_code != 200 or response is None:
            raise Exception(f"Request failed, cause of {response.reason}")

        return response.json()
