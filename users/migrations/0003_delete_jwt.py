# Generated by Django 4.0.6 on 2022-07-08 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_jwt'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Jwt',
        ),
    ]
