# Generated by Django 3.2.9 on 2022-08-23 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0005_restaurant_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='cuisines',
        ),
    ]
