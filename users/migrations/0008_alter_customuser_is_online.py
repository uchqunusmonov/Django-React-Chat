# Generated by Django 4.0.6 on 2022-07-11 09:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_customuser_is_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_online',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 11, 9, 15, 46, 725124, tzinfo=utc)),
        ),
    ]
