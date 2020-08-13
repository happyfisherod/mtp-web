# Generated by Django 3.0.3 on 2020-08-02 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guidebook', '0008_pointofinterest'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointofinterest',
            name='point_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='pointofinterest',
            name='position_x',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pointofinterest',
            name='position_y',
            field=models.FloatField(default=0),
        ),
    ]
