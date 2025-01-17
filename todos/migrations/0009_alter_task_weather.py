# Generated by Django 5.0.6 on 2024-05-29 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0008_weather_task_weather'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='weather',
            field=models.ForeignKey(blank=True, db_comment='Weather for the location', null=True, on_delete=django.db.models.deletion.CASCADE, to='todos.weather'),
        ),
    ]
