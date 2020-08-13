# Generated by Django 3.0.3 on 2020-07-23 22:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0015_auto_20200722_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddField(
            model_name='photographer',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
