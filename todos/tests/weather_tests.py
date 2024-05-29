import pytest

from todos.models import Weather

@pytest.mark.django_db
def test_weather_model():
    weather = Weather.objects.create(
        id=1,
        temperature=290.0,
        humidity=50,
        condition=800,
        latitude=0.0,
        longitude=0.0,
    )
    assert str(weather) == "16°C, 50% humidity"
    assert weather.temperature_celsius() == 16
    assert weather.as_dictionary() == {
        "id": 1,
        "temperature": 290.0,
        "condition": 800,
        "humidity": 50,
        "latitude": 0.0,
        "longitude": 0.0,
        "description": {
            "title": "16°C, 50% humidity",
            "condition": {"color": "yellow", "name": "Clear sky"}
        },
    }

@pytest.mark.django_db
@pytest.mark.parametrize("condition, expected", [
    (800, {"color": "yellow", "name": "Clear sky"}),
    (804, {"color": "violet", "name": "Overcast clouds"}),
    (803, {"color": "sandybrown", "name": "Broken clouds"}),
    (802, {"color": "thistle", "name": "Scattered clouds"}),
    (801, {"color": "turquoise", "name": "Few clouds"}),
    (800, {"color": "yellow", "name": "Clear sky"}),
    (701, {"color": "green", "name": "Atmosphere"}),
    (600, {"color": "darkred", "name": "Snow"}),
    (500, {"color": "slateblue", "name": "Rain"}),
    (300, {"color": "blue", "name": "Drizzle"}),
    (200, {"color": "purple", "name": "Thunderstorm"}),
])
def test_weather_condition_map(condition, expected):
    weather = Weather.objects.create(
        temperature=290.0,
        humidity=50,
        condition=condition,
        latitude=0.0,
        longitude=0.0,
    )

    assert weather.condition_map() == expected, f"Condition {condition} failed"
