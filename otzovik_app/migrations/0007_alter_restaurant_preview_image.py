# Generated by Django 3.2.9 on 2022-08-23 12:08

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('otzovik_app', '0006_remove_restaurant_cuisines'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='preview_image',
            field=django_resized.forms.ResizedImageField(crop=None, default='grey.jpg', force_format=None, keep_meta=True, quality=-1, scale=None, size=[640, 360], upload_to='preview_images'),
        ),
    ]
