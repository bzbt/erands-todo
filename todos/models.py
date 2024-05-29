import uuid

from django.db import models

from weather.api.client import RawWeather


class Task(models.Model):
    """
    Model representing a task.

    Attributes:
        public_id: Public identifier of the task
        title: Title of the task
        description: Description of the task
        location: Location of the task
        weather: Weather for the location
        user: User who created the task
        complete: Whether the task is complete
        deleted: Whether the task is deleted
        created: Date and time the task was created
        updated: Date and time the task was last updated
    """
    public_id = models.UUIDField(
        default=uuid.uuid4, editable=False, db_comment="Public identifier of the task"
    )
    title = models.CharField(max_length=200, db_comment="Title of the task")
    description = models.TextField(blank=True, db_comment="Description of the task")
    location = models.ForeignKey(
        "todos.Location",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_comment="Location of the task",
    )
    weather = models.ForeignKey(
        "todos.Weather",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_comment="Weather for the location",
    )
    user = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, db_comment="User who created the task"
    )
    complete = models.BooleanField(
        default=False, db_comment="Whether the task is complete"
    )
    deleted = models.BooleanField(
        default=False, db_comment="Whether the task is deleted"
    )
    created = models.DateTimeField(
        auto_now_add=True, db_comment="Date and time the task was created"
    )
    updated = models.DateTimeField(
        auto_now=True, db_comment="Date and time the task was last updated"
    )

    def __str__(self):
        return self.title


class Location(models.Model):
    """
    Model representing a location.

    Attributes:
        city: Name of the city
        country: Name of the country
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    city = models.CharField(max_length=255, db_comment="Name of the city")
    country = models.CharField(max_length=255, db_comment="Name of the country")
    latitude = models.FloatField(db_comment="Latitude of the location")
    longitude = models.FloatField(db_comment="Longitude of the location")

    def __str__(self):
        return self.city + ", " + self.country


class Weather(models.Model):
    """
    Model representing weather data.

    Attributes:
        temperature: Temperature in Kelvin
        humidity: Humidity in percent
        condition: Weather condition code
        latitude: Latitude of the location
        longitude: Longitude of the location
        created: Date and time the task was created
        updated: Date and time the task was last updated
    """
    temperature = models.FloatField(db_comment="Temperature in Kelvin")
    humidity = models.IntegerField(db_comment="Humidity in percent")
    condition = models.IntegerField(default=0, db_comment="Weather condition code")
    latitude = models.FloatField(default=0, db_comment="Latitude of the location")
    longitude = models.FloatField(default=0, db_comment="Longitude of the location")
    created = models.DateTimeField(
        auto_now_add=True, db_comment="Date and time the task was created"
    )
    updated = models.DateTimeField(
        auto_now=True, db_comment="Date and time the task was last updated"
    )

    def __str__(self):
        return f"{self.temperature_celsius()}°C, {self.humidity}% humidity"

    def temperature_celsius(self) -> int:
        """
        Returns the temperature in Celsius

        Returns:
            int: The temperature in Celsius
        """
        return int(self.temperature - 273.15)

    def condition_map(self) -> dict[str, str] | None:
        """
        Returns the color and name of the weather conditions, if available in the condition map

        Returns:
            dict[str, str] | None: The color and name of the weather conditions, or None if not available
        """
        condition_map = {
            range(200, 300): {"color": "purple", "name": "Thunderstorm"},
            range(300, 500): {"color": "blue", "name": "Drizzle"},
            range(500, 600): {"color": "slateblue", "name": "Rain"},
            range(600, 700): {"color": "darkred", "name": "Snow"},
            range(700, 800): {"color": "green", "name": "Atmosphere"},
            800: {"color": "yellow", "name": "Clear sky"},
            801: {"color": "turquoise", "name": "Few clouds"},
            802: {"color": "thistle", "name": "Scattered clouds"},
            803: {"color": "sandybrown", "name": "Broken clouds"},
            804: {"color": "violet", "name": "Overcast clouds"},
        }
        if self.condition not in range(200, 805):
            return None

        for condition_range, condition in condition_map.items():
            if type(condition_range) is int and self.condition == condition_range:
                return condition
            elif type(condition_range) is range and self.condition in condition_range:
                return condition

    def from_raw(self, data: RawWeather, id: int = None):
        """
        Creates a Weather object from raw weather data

        Args:
            data (RawWeather): The raw weather data
            id   (int):        The ID of the weather data
        """
        if id is not None:
            self.id = id
        self.temperature = data.temperature
        self.humidity = data.humidity
        self.condition = data.condition
        self.latitude = data.latitude
        self.longitude = data.longitude
        return self

    def as_dictionary(self):
        """
        Returns the weather data as a dictionary

        Returns:
            dict: The weather data as a dictionary
        """
        return {
            "id": self.id,
            "condition": self.condition,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": {
                "title": str(self),
                "condition": self.condition_map(),
            },
        }
