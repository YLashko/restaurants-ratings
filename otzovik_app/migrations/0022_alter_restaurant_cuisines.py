# Generated by Django 3.2.9 on 2022-09-12 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0021_alter_restaurant_cuisines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='cuisines',
            field=models.ManyToManyField(related_name='restaurant', to='otzovik_app.RestaurantCuisine'),
        ),
    ]
