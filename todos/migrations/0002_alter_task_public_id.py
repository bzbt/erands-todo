# Generated by Django 5.0.6 on 2024-05-25 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="public_id",
            field=models.UUIDField(
                db_comment="Public identifier of the task", editable=False
            ),
        ),
    ]
