# Generated by Django 5.0.6 on 2024-05-24 19:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.CharField(db_comment='Public identifier for the task', max_length=200, unique=True)),
                ('title', models.CharField(db_comment='Title of the task', max_length=200)),
                ('description', models.TextField(blank=True, db_comment='Description of the task')),
                ('complete', models.BooleanField(db_comment='Whether the task is complete', default=False)),
                ('created', models.DateTimeField(auto_now_add=True, db_comment='Date and time the task was created')),
                ('updated', models.DateTimeField(auto_now=True, db_comment='Date and time the task was last updated')),
                ('user', models.ForeignKey(db_comment='User who created the task', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]