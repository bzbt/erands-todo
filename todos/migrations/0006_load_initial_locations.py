# Generated by Django 5.0.6 on 2024-05-26 10:03

from django.db import migrations


def load_initial_data(apps, schema_editor):
    location = apps.get_model('todos', 'Location')

    locations = [
        {"city": "London", "country": "UK", "latitude": 51.5073219, "longitude": -0.1276474},
        {'city': 'Paris', 'country': 'France', 'latitude': 48.8588897, 'longitude': 2.3200410217200766},
        {"city": "Berlin", "country": "Germany", "latitude": 52.5170365, "longitude": 13.3888599},
        {'city': 'New York', 'country': 'USA', 'latitude': 40.7127281, 'longitude': -74.0060152},
        {'city': 'Tokyo', 'country': 'Japan', 'latitude': 35.6828387, 'longitude': 139.7594549},
        {'city': 'Sydney', 'country': 'Australia', 'latitude': -33.8698439, 'longitude': 151.2082848},
        {"city": 'Cape Town', "country": "South Africa", "latitude": -33.928992, "longitude": 18.417396},
        {"city": "Rio de Janeiro", "country": "Brazil", "latitude": -22.9110137, "longitude": -43.2093727},
        {"city": "Warsaw", "country": "Poland", "latitude": 52.2319581, "longitude": 21.0067249},
    ]
    for loc in locations:
        location.objects.create(**loc)


class Migration(migrations.Migration):
    dependencies = [
        ('todos', '0005_location'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
