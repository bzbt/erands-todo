import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0006_load_initial_locations'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='location',
            field=models.ForeignKey(blank=True, db_comment='Location of the task', null=True, on_delete=django.db.models.deletion.CASCADE, to='todos.location'),
        ),
    ]
