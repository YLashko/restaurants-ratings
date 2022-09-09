# Generated by Django 3.2.9 on 2022-09-05 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0016_reviewsummary'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='cuisines',
            field=models.ManyToManyField(related_name='restaurant', to='otzovik_app.RestaurantCuisine'),
        ),
    ]
